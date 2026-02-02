from django.contrib import admin
from .models import Carta, Colecao, Posse, Lista
from django.utils.html import format_html
from django.db.models import Count

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    """Personaliza a admin de Carta para melhor visualização e filtro."""
    list_display = ('nome', 'printing', 'raridade', 'tipo', 'imagem_display')
    search_fields = ('nome', 'printing')
    list_filter = ('printing', 'raridade', 'tipo')

    def imagem_display(self, obj):
        if obj.imagem:
            return format_html(f'<img src="{obj.imagem.url}" style="max-height: 100px;" />')
        return "N/A"
    imagem_display.short_description = 'Imagem'

class PosseInline(admin.TabularInline):
    """Define a visualização inline das Posses dentro de uma Coleção."""
    model = Posse
    # Usar raw_id_fields para 'carta' melhora a performance,
    # substituindo um dropdown por um campo de busca.
    raw_id_fields = ('carta',)
    # Campos que aparecerão no formulário inline
    fields = ('carta', 'estado_carta', 'status', 'preco_usd', 'imagem_display')
    readonly_fields = ('imagem_display',)
    extra = 0  # Não mostrar formulários extras em branco por padrão

    # Método para mostrar a imagem da carta relacionada
    def imagem_display(self, obj):
        if obj.carta and obj.carta.imagem:
            return format_html(f'<img src="{obj.carta.imagem.url}" style="max-height: 100px;" />')
        return "N/A"
    imagem_display.short_description = 'Imagem da Carta'

@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    """Personaliza a admin da Coleção para incluir as posses como inlines."""
    list_display = ('usuario', 'total_de_posses')
    inlines = [PosseInline]
    search_fields = ('usuario__username',)

    def get_queryset(self, request):
        # Otimiza a consulta para contar as posses de forma eficiente
        queryset = super().get_queryset(request)
        return queryset.annotate(total_posses=Count('posse'))

    @admin.display(description='Total de Cartas na Coleção', ordering='total_posses')
    def total_de_posses(self, obj):
        return obj.total_posses

@admin.register(Posse)
class PosseAdmin(admin.ModelAdmin):
    """Personaliza a admin de Posse para uma listagem mais informativa."""
    list_display = ('id', 'get_usuario', 'get_card_nome', 'get_card_printing', 'estado_carta', 'status', 'preco_usd')
    list_filter = ('status', 'estado_carta', 'carta__printing')
    search_fields = ('carta__nome', 'colecao__usuario__username')
    raw_id_fields = ('carta', 'colecao')

    def get_queryset(self, request):
        # Otimiza a query para buscar informações relacionadas de uma só vez
        return super().get_queryset(request).select_related('colecao__usuario', 'carta')

    @admin.display(description='Usuário', ordering='colecao__usuario__username')
    def get_usuario(self, obj):
        return obj.colecao.usuario.username

    @admin.display(description='Carta', ordering='carta__nome')
    def get_card_nome(self, obj):
        return obj.carta.nome

    @admin.display(description='Printing', ordering='carta__printing')
    def get_card_printing(self, obj):
        return obj.carta.printing

# Registra o modelo Lista, que não precisa de personalização complexa
admin.site.register(Lista)
