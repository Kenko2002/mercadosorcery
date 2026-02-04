from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SocialEntity

class SocialEntityCreationForm(UserCreationForm):
    """
    Um formulário para criar novos usuários sem a necessidade de um username.
    """
    class Meta(UserCreationForm.Meta):
        model = SocialEntity
        fields = ('email', 'first_name', 'last_name', 'cpf', 'role')

class SocialEntityChangeForm(UserChangeForm):
    """
    Um formulário para atualizar usuários existentes sem um username.
    """
    class Meta:
        model = SocialEntity
        fields = ('email', 'first_name', 'last_name', 'cpf', 'role', 'imagem', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
