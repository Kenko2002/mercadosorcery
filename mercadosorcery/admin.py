from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Carta, Colecao, Posse, Lista

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'printing', 'raridade', 'tipo', 'display_image')
    list_filter = ('printing', 'raridade', 'tipo')
    search_fields = ('nome',)

    def display_image(self, obj):
        if obj.imagem:
            # Gera a URL para a view que serve a imagem
            image_url = reverse('card_image', args=[obj.id])
            return format_html(f'<img src="{image_url}" width="60" height="84" />')
        return "Sem imagem"
    display_image.short_description = "Imagem"

@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__first_name', 'usuario__last_name', 'usuario__email')

@admin.register(Posse)
class PosseAdmin(admin.ModelAdmin):
    list_display = ('carta', 'colecao', 'status', 'estado_carta', 'preco_usd')
    list_filter = ('status', 'estado_carta', 'colecao__usuario')
    search_fields = ('carta__nome', 'colecao__usuario__first_name', 'colecao__usuario__last_name')

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')
    search_fields = ('nome', 'usuario__first_name', 'usuario__last_name')
