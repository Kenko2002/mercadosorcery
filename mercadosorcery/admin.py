from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Carta, Colecao, Posse, Lista

# Classe Inline para o modelo Posse
class PosseInline(admin.TabularInline):
    model = Posse
    extra = 1  # Quantidade de formulários extras para adicionar
    
    # Campo para mostrar a prévia da imagem da carta
    readonly_fields = ('image_preview',)
    
    # Lista de campos a serem exibidos no inline
    fields = ('carta', 'image_preview', 'status', 'estado_carta', 'preco_usd')
    
    # Usar um widget de busca para o campo 'carta' para melhorar a performance
    raw_id_fields = ('carta',)

    def image_preview(self, obj):
        # Verifica se a Posse tem uma Carta associada e se a Carta tem uma imagem
        if obj.carta and obj.carta.imagem:
            # Gera a URL para a view que serve a imagem da carta
            image_url = reverse('card_image', args=[obj.carta.id])
            return format_html(f'<img src="{image_url}" width="60" height="84" />')
        return "Sem imagem"
    image_preview.short_description = "Prévia da Imagem"

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'printing', 'raridade', 'tipo', 'display_image')
    list_filter = ('printing', 'raridade', 'tipo')
    search_fields = ('nome',)

    def display_image(self, obj):
        if obj.imagem:
            image_url = reverse('card_image', args=[obj.id])
            return format_html(f'<img src="{image_url}" width="60" height="84" />')
        return "Sem imagem"
    display_image.short_description = "Imagem"

@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__first_name', 'usuario__last_name', 'usuario__email')
    # Adiciona o inline de Posse na página de edição da Coleção
    inlines = [PosseInline]

@admin.register(Posse)
class PosseAdmin(admin.ModelAdmin):
    list_display = ('carta', 'colecao', 'status', 'estado_carta', 'preco_usd', 'image_preview')
    list_filter = ('status', 'estado_carta', 'colecao__usuario')
    search_fields = ('carta__nome', 'colecao__usuario__first_name', 'colecao__usuario__last_name')
    raw_id_fields = ('carta',)

    def image_preview(self, obj):
        if obj.carta and obj.carta.imagem:
            image_url = reverse('card_image', args=[obj.carta.id])
            return format_html(f'<a href="{image_url}" target="_blank"><img src="{image_url}" width="60" height="84" /></a>')
        return "Sem imagem"
    image_preview.short_description = "Prévia da Imagem"


# Ajuste para Lista, que tem um ManyToMany com Posse
class ListaPosseInline(admin.TabularInline):
    model = Lista.cartas.through # Acessa a tabela intermediária do ManyToMany
    extra = 1
    verbose_name = "Posse na Lista"
    verbose_name_plural = "Posses na Lista"
    
    # Campos a serem exibidos
    fields = ('posse', 'image_preview')
    readonly_fields = ('image_preview',)
    raw_id_fields = ('posse',)

    def image_preview(self, obj):
        # O obj aqui é a entrada da tabela intermediária
        if obj.posse and obj.posse.carta and obj.posse.carta.imagem:
            image_url = reverse('card_image', args=[obj.posse.carta.id])
            return format_html(f'<img src="{image_url}" width="60" height="84" />')
        return "Sem imagem"
    image_preview.short_description = "Prévia da Imagem"


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')
    search_fields = ('nome', 'usuario__first_name', 'usuario__last_name')
    # Exclui o campo 'cartas' padrão para evitar confusão com o inline
    exclude = ('cartas',)
    # Adiciona o inline customizado
    inlines = [ListaPosseInline]
