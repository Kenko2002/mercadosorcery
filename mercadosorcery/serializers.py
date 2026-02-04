from rest_framework import serializers
from .models import Carta, Colecao, Posse, Lista

class CriarPosseSerializer(serializers.Serializer):
    """
    Serializer para validar a entrada da criação de novas posses.
    """
    carta_id = serializers.IntegerField(required=True)
    quantidade = serializers.IntegerField(min_value=1, default=1)
    estado_carta = serializers.ChoiceField(choices=Posse.EstadoCarta.choices, default=Posse.EstadoCarta.NEAR_MINT)
    status = serializers.ChoiceField(choices=Posse.Status.choices, default=Posse.Status.FORA_DE_VENDA)
    preco_usd = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)

    def validate_carta_id(self, value):
        """
        Verifica se a carta com o ID fornecido existe.
        """
        if not Carta.objects.filter(id=value).exists():
            raise serializers.ValidationError("Carta com o ID fornecido não existe.")
        return value

class CartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = '__all__'

class PosseSerializer(serializers.ModelSerializer):
    carta = CartaSerializer(read_only=True)
    class Meta:
        model = Posse
        fields = '__all__'

class ColecaoSerializer(serializers.ModelSerializer):
    cartas = PosseSerializer(many=True, read_only=True, source='posse_set')
    class Meta:
        model = Colecao
        fields = '__all__'

class ListaSerializer(serializers.ModelSerializer):
    cartas = PosseSerializer(many=True, read_only=True)
    class Meta:
        model = Lista
        fields = '__all__'

class MinhaColecaoSerializer(serializers.ModelSerializer):
    """
    Serializer para a representação agregada das posses de um usuário.
    """
    carta = CartaSerializer(read_only=True)
    quantidade = serializers.IntegerField(read_only=True)
    posse_ids = serializers.ListField(
        child=serializers.IntegerField(), read_only=True
    )

    class Meta:
        model = Posse
        fields = ['carta', 'estado_carta', 'status', 'preco_usd', 'quantidade', 'posse_ids']
