from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SocialEntity

@admin.register(SocialEntity)
class SocialEntityAdmin(UserAdmin):
    """
    Configuração do painel de administração para SocialEntity.
    Herda de UserAdmin para aproveitar a maior parte da funcionalidade padrão.
    """
    # A ordem dos campos na lista de usuários
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'cpf')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')

    # Usa os fieldsets padrão do UserAdmin, mas ajustados para nosso modelo
    # Removendo 'username' e adicionando 'cpf', 'role', 'imagem'
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações Pessoais", {"fields": ("first_name", "last_name", "cpf", "role", "imagem")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Fieldset para a criação de um novo usuário. A senha precisa de um campo de confirmação.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "password2", "first_name", "last_name", "cpf", "role"),
        }),
    )

    # O campo de ordenação
    ordering = ("email",)
