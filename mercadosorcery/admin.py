from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
import os
from .models import Usuario, Carta, Colecao, Posse, Lista

# --- Configuração do Perfil Inline (para Usuários) ---
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fk_name = 'user'

# --- Inlines para exibir cartas com imagens em Coleções e Listas ---

class PosseInline(admin.TabularInline):
    """
    Exibe as posses de uma coleção com imagens, usando a configuração de arquivos estáticos.
    """
    model = Posse
    extra = 0
    readonly_fields = ('imagem_da_carta', 'detalhes_da_carta', 'estado_carta', 'status', 'preco_usd')
    fields = ('imagem_da_carta', 'detalhes_da_carta', 'estado_carta', 'status', 'preco_usd')

    def detalhes_da_carta(self, obj):
        return f"{obj.carta.nome} ({obj.carta.printing})"
    detalhes_da_carta.short_description = 'Carta'

    def imagem_da_carta(self, obj):
        if obj.carta and obj.carta.imagem:
            nome_arquivo = os.path.basename(obj.carta.imagem)
            url_imagem = f"{settings.STATIC_URL}{nome_arquivo}"
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', url_imagem)
        return "Sem Imagem"
    imagem_da_carta.short_description = 'Imagem'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CartasNaListaInline(admin.TabularInline):
    """
    Permite adicionar/remover posses de uma lista, exibindo a imagem via arquivos estáticos.
    """
    model = Lista.cartas.through
    extra = 1
    verbose_name = "Carta na Lista"
    verbose_name_plural = "Cartas na Lista"
    autocomplete_fields = ('posse',)
    readonly_fields = ('imagem_da_carta',)
    fields = ('posse', 'imagem_da_carta',)

    def imagem_da_carta(self, obj):
        if obj.posse and obj.posse.carta and obj.posse.carta.imagem:
            nome_arquivo = os.path.basename(obj.posse.carta.imagem)
            url_imagem = f"{settings.STATIC_URL}{nome_arquivo}"
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', url_imagem)
        return ""
    imagem_da_carta.short_description = 'Imagem'


# --- Registrando os modelos e aplicando os inlines ---

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('imagem_da_carta', 'nome', 'printing', 'rarity', 'cmc')
    search_fields = ('nome', 'printing')
    list_filter = ('rarity', 'printing')

    def imagem_da_carta(self, obj):
        if obj.imagem:
            nome_arquivo = os.path.basename(obj.imagem)
            url_imagem = f"{settings.STATIC_URL}{nome_arquivo}"
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', url_imagem)
        return "Sem Imagem"
    imagem_da_carta.short_description = 'Imagem'

@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    search_fields = ('usuario__email',)
    inlines = [PosseInline]

@admin.register(Posse)
class PosseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'colecao', 'estado_carta', 'status')
    search_fields = ('carta__nome', 'colecao__usuario__email')
    list_filter = ('estado_carta', 'status')

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')
    search_fields = ('nome', 'usuario__email')
    inlines = [CartasNaListaInline]
    exclude = ('cartas',)
