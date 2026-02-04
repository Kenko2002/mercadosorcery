import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import SocialEntityManager

class SocialEntity(AbstractUser):
    """
    Modelo de usuário customizado. A restrição 'unique' do CPF foi removida
    para permitir a criação em 2 etapas. A unicidade é garantida pelo formulário.
    """
    class Role(models.TextChoices):
        PACIENTE = 'PACIENTE', 'Paciente'
        MEDICO = 'MEDICO', 'Medico'

    username = None
    email = models.EmailField('endereço de email', unique=True)
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf', 'role']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # unique=True foi REMOVIDO daqui para consertar o bug da criação de usuário.
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)
    imagem = models.ImageField(upload_to='imagens_perfil/', blank=True, null=True)
    role = models.CharField('função', max_length=50, choices=Role.choices, null=True, blank=True)

    objects = SocialEntityManager()

    def __str__(self):
        return self.email
