import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import SocialEntityManager

class SocialEntity(AbstractUser):
    """
    Modelo de usuário customizado.
    Reintroduzindo o 'username' para estabilidade com o Django Admin, 
    mas mantendo o email como o principal meio de login.
    """
    # O username está de volta para compatibilidade.
    # O AbstractUser já define o username, então só precisamos garantir
    # que nossas configurações e managers o utilizem corretamente.
    
    # O email ainda é o campo de login e deve ser único.
    email = models.EmailField('endereço de email', unique=True)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # O email será usado para o login
    USERNAME_FIELD = 'email'
    # O username será um campo obrigatório no momento da criação (ex: createsuperuser)
    REQUIRED_FIELDS = ['username']

    objects = SocialEntityManager()

    def __str__(self):
        return self.email
