from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SocialEntity
from .forms import SocialEntityCreationForm, SocialEntityChangeForm # Importando os formulários

@admin.register(SocialEntity)
class SocialEntityAdmin(UserAdmin):
    """
    Configuração do painel de administração para o modelo SocialEntity.
    """
    # Informa ao Django para usar nossos formulários customizados
    form = SocialEntityChangeForm
    add_form = SocialEntityCreationForm

    # Campos exibidos na lista de usuários
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    # Campos pelos quais a lista pode ser pesquisada
    search_fields = ('email', 'first_name', 'last_name')
    # Filtros disponíveis na barra lateral
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    
    # Campos a serem exibidos no formulário de edição do usuário
    # Importante: Removendo 'username' se ele estiver aqui por herança
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'cpf', 'role', 'imagem')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos que devem ser preenchidos no formulário de criação
    # Isso é controlado pelo add_form agora, mas é bom manter para clareza
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'cpf', 'role'),
        }),
    )
    
    # O campo usado para ordenação
    ordering = ('email',)
