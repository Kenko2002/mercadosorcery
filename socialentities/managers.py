from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class SocialEntityManager(BaseUserManager):
    """
    Manager customizado para o modelo de usuário, onde o email é o identificador único.
    """
    def create_user(self, email, password, first_name, last_name, cpf, role, **extra_fields):
        """
        Cria e salva um usuário com o email, senha e outros campos obrigatórios.
        """
        if not email:
            raise ValueError(_('O Endereço de email deve ser fornecido'))
        if not first_name:
            raise ValueError(_('O Primeiro nome deve ser fornecido'))
        if not last_name:
            raise ValueError(_('O Último nome deve ser fornecido'))
        if not cpf:
            raise ValueError(_('O CPF deve ser fornecido'))
        if not role:
            raise ValueError(_('A Função (role) deve ser fornecida'))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            cpf=cpf,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário deve ter is_superuser=True.'))

        # Define valores padrão para os campos que não são solicitados ao criar um superuser pela linha de comando
        # mas que são obrigatórios no nosso método create_user.
        return self.create_user(
            email,
            password,
            first_name=extra_fields.pop('first_name', 'Admin'),
            last_name=extra_fields.pop('last_name', 'System'),
            cpf=extra_fields.pop('cpf', '00000000000'),
            role=extra_fields.pop('role', 'MEDICO'),
            **extra_fields
        )
