from django.contrib.auth.models import BaseUserManager

class SocialEntityManager(BaseUserManager):
    """
    Gerenciador customizado para o modelo SocialEntity, onde o email é o identificador único
    em vez do username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError('O Email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        # Para o comando createsuperuser, os campos requeridos (first_name, last_name) não são passados por padrão
        # então provemos valores padrão se não estiverem presentes.
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('role', 'MEDICO') # Ou qualquer role padrão que faça sentido
        extra_fields.setdefault('cpf', '00000000000') # Um CPF placeholder

        return self.create_user(email, password, **extra_fields)
