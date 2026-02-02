import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import SocialEntityManager # Importa o novo gerenciador

class SocialEntity(AbstractUser):
    """
    Modelo de usuário customizado que representa todos os usuários do sistema.
    """
    class Role(models.TextChoices):
        PACIENTE = 'PACIENTE', 'Paciente'
        MEDICO = 'MEDICO', 'Medico'

    # Remove o username e define o email como o campo de login
    username = None
    email = models.EmailField('endereço de email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Campos customizados
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    imagem = models.ImageField(upload_to='imagens_perfil/', blank=True, null=True)
    role = models.CharField('função', max_length=50, choices=Role.choices)

    # Conecta o gerenciador customizado ao modelo
    objects = SocialEntityManager()

    def __str__(self):
        return self.email
