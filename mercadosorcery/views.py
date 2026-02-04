from collections import defaultdict
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.management import call_command

from .models import Carta, Colecao, Posse, Lista
from .serializers import (
    CartaSerializer, ColecaoSerializer, PosseSerializer, ListaSerializer,
    CriarPosseSerializer, MinhaColecaoSerializer
)


class PopulateCardsView(APIView):
    """
    Um endpoint para acionar o comando de popular o banco de dados com as cartas.
    Acesso restrito a administradores.
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Aciona o script para popular o banco de dados com os dados das cartas do Scryfall.",
        responses={200: "Comando executado com sucesso.", 500: "Ocorreu um erro ao executar o comando."}
    )
    def get(self, request):
        try:
            # Chama o comando de gerenciamento
            call_command('populate_cards')
            return Response({"status": "O comando para popular o banco de dados foi executado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Ocorreu um erro ao executar o comando: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdicionarPosseView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CriarPosseSerializer,
        operation_description="Adiciona uma ou mais cópias de uma carta à coleção do usuário autenticado."
    )
    def post(self, request):
        serializer = CriarPosseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            carta = Carta.objects.get(id=data['carta_id'])
            colecao, _ = Colecao.objects.get_or_create(usuario=request.user)

            possessions_to_create = [
                Posse(
                    carta=carta,
                    colecao=colecao,
                    estado_carta=data['estado_carta'],
                    status=data['status'],
                    preco_usd=data.get('preco_usd')
                )
                for _ in range(data['quantidade'])
            ]

            Posse.objects.bulk_create(possessions_to_create)

            return Response(
                {'status': f'{data["quantidade"]} cópias da carta {carta.nome} foram adicionadas à sua coleção.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class MinhaColecaoView(APIView):
    """
    Lista a coleção de cartas do usuário autenticado, agrupando posses idênticas.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Retorna a coleção do usuário, com as cartas agrupadas. Permite filtrar por nome da carta e uma ou mais edições.",
        manual_parameters=[
            openapi.Parameter('nome', openapi.IN_QUERY, description="Filtra as cartas pelo nome (case-insensitive).", type=openapi.TYPE_STRING),
            openapi.Parameter('printings', openapi.IN_QUERY, description="Filtra por uma ou mais edições, separadas por vírgula (ex: 'BET,ART').", type=openapi.TYPE_STRING),
        ],
        responses={200: MinhaColecaoSerializer(many=True)}
    )
    def get(self, request):
        try:
            colecao = Colecao.objects.get(usuario=request.user)
            queryset = Posse.objects.filter(colecao=colecao).select_related('carta')
        except Colecao.DoesNotExist:
            queryset = Posse.objects.none()

        nome_carta = request.query_params.get('nome', None)
        if nome_carta:
            queryset = queryset.filter(carta__nome__icontains=nome_carta)

        printings_param = request.query_params.get('printings', None) or request.query_params.get('printing', None)
        if printings_param:
            printings = [p.strip().upper() for p in printings_param.split(',')]
            queryset = queryset.filter(carta__printing__in=printings)

        # Agrupamento manual em Python para evitar dependência do ArrayAgg do Postgres
        grouped_possessions = defaultdict(lambda: {'posse_ids': [], 'quantidade': 0})
        ordered_queryset = queryset.order_by('carta_id', 'estado_carta', 'status', 'preco_usd')

        for posse in ordered_queryset:
            group_key = (
                posse.carta_id,
                posse.estado_carta,
                posse.status,
                posse.preco_usd
            )
            
            if not grouped_possessions[group_key]['posse_ids']:
                grouped_possessions[group_key]['carta'] = posse.carta
                grouped_possessions[group_key]['estado_carta'] = posse.estado_carta
                grouped_possessions[group_key]['status'] = posse.status
                grouped_possessions[group_key]['preco_usd'] = posse.preco_usd
            
            grouped_possessions[group_key]['posse_ids'].append(posse.id)
            grouped_possessions[group_key]['quantidade'] += 1

        results = list(grouped_possessions.values())
        
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(results, request, view=self)
        
        serializer = MinhaColecaoSerializer(paginated_results, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class CartaViewSet(viewsets.ModelViewSet):
    queryset = Carta.objects.all()
    serializer_class = CartaSerializer

class ColecaoViewSet(viewsets.ModelViewSet):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer

class PosseViewSet(viewsets.ModelViewSet):
    queryset = Posse.objects.all()
    serializer_class = PosseSerializer

class ListaViewSet(viewsets.ModelViewSet):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer
