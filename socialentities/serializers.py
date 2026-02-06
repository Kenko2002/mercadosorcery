from rest_framework import serializers
from .models import SocialEntity
from django.contrib.auth import authenticate

class SocialEntitySerializer(serializers.ModelSerializer):
    """
    Serializador para visualização e atualização de instâncias de SocialEntity.
    """
    class Meta:
        model = SocialEntity
        fields = ("__all__")
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializador para o processo de registro de novos usuários.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = SocialEntity
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        # Usa o método create_user do nosso modelo para garantir que a senha seja hasheada
        user = SocialEntity.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializador para o endpoint de login. Não é baseado em um modelo.
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get("request")

        # A chamada authenticate requer um objeto request, que não está disponível
        # durante a geração do schema pelo drf-yasg. Pulamos a validação se o
        # request não estiver no contexto.
        if not request:
            # Para a geração do schema, podemos retornar os atributos sem validação.
            # Adicionamos 'user' como None para manter a consistência do retorno.
            attrs['user'] = None
            return attrs

        if email and password:
            user = authenticate(request=request, email=email, password=password)

            if not user:
                msg = 'Não foi possível fazer login com as credenciais fornecidas.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'É necessário incluir "email" e "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
