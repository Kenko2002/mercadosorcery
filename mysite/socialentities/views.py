from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .models import SocialEntity
from .serializers import SocialEntitySerializer, UserRegistrationSerializer, LoginSerializer

class SocialEntityViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o CRUD de SocialEntity.
    - `list`: Retorna todos os usuários (requer autenticação).
    - `retrieve`: Retorna um usuário específico (requer autenticação).
    - `update`/`partial_update`: Atualiza um usuário (requer autenticação).
    - `destroy`: Deleta um usuário (requer autenticação).
    - `create`: Utiliza o UserRegistrationSerializer para registrar um novo usuário (aberto).
    """
    queryset = SocialEntity.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return SocialEntitySerializer

    def get_permissions(self):
        """
        Permite acesso anônimo para criar (registrar) um novo usuário.
        Para todas as outras ações, exige que o usuário esteja autenticado.
        """
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super(SocialEntityViewSet, self).get_permissions()

class LoginView(APIView):
    """
    View para realizar o login do usuário e retornar um token de autenticação.
    """
    permission_classes = [AllowAny] # Qualquer um pode tentar fazer login

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email}, status=status.HTTP_200_OK)

class MeView(APIView):
    """
    View que retorna os dados do usuário autenticado (logado).
    """
    permission_classes = [IsAuthenticated] # Apenas usuários autenticados podem acessar

    def get(self, request, format=None):
        """
        Retorna o objeto do usuário logado.
        """
        serializer = SocialEntitySerializer(request.user)
        return Response(serializer.data)
