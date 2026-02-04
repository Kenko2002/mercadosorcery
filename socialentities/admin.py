from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SocialEntity
from mercadosorcery.admin import UsuarioInline

@admin.register(SocialEntity)
class SocialEntityAdmin(UserAdmin):
    """
    Configuração do Admin para SocialEntity.
    Com o retorno do campo 'username', podemos simplificar drasticamente,
    removendo os formulários customizados e herdando diretamente do UserAdmin.
    """
    inlines = (UsuarioInline,)

    # Apenas precisamos garantir que o 'email' apareça na lista e nos fieldsets,
    # pois já é o USERNAME_FIELD.
    # O UserAdmin padrão cuida do resto.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Adicionando 'email' ao fieldset de informações pessoais do UserAdmin padrão
    # A estrutura dos fieldsets é herdada, vamos apenas modificá-la
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Adicionais', {'fields': ('id',)}), # Adicionando o UUID se quiser vê-lo
    )
    readonly_fields = ('id', 'last_login', 'date_joined')
