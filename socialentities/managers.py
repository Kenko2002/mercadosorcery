from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class SocialEntityManager(BaseUserManager):
    """
    Manager customizado para o modelo de usuário, onde o email é o identificador único.
    Esta versão é flexível para funcionar com o fluxo de criação do Django Admin.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos. Aceita campos extras.
        """
        if not email:
            raise ValueError(_('O Endereço de email deve ser fornecido'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Cria e salva um superusuário com email, senha e permissões de staff/superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário deve ter is_superuser=True.'))

        # Para o comando createsuperuser, garante que os campos requeridos pelo prompt
        # sejam passados para o create_user.
        return self.create_user(email, password, **extra_fields)
