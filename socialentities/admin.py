from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SocialEntity
from .forms import SocialEntityCreationForm, SocialEntityChangeForm # Importando os formulários corretos

@admin.register(SocialEntity)
class SocialEntityAdmin(UserAdmin):
    """
    Configuração do admin que utiliza formulários customizados para suportar o SocialEntity.
    Esta é a abordagem correta e definitiva.
    """
    # 1. Usa o formulário de CRIAÇÃO customizado (Etapa 1)
    add_form = SocialEntityCreationForm
    
    # 2. Usa o formulário de EDIÇÃO customizado (Etapa 2)
    form = SocialEntityChangeForm
    
    # 3. Informa ao Django qual é o modelo que este admin gerencia
    model = SocialEntity

    # Campos exibidos na lista de usuários (sem alteração)
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    
    # Mantém a estrutura de fieldsets para a página de edição
    # O `form` (SocialEntityChangeForm) já define os campos, mas o fieldsets organiza a UI
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações Pessoais", {"fields": ("first_name", "last_name", "cpf", "role", "imagem")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    # A página de criação (add_form) só precisa de um fieldset mínimo
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "password2"),
        }),
    )
    
    # Configurações adicionais (sem alteração)
    search_fields = ('email', 'first_name', 'last_name', 'cpf')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('email',)
