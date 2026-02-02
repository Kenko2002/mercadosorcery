from django.urls import path
from .views import AdicionarPosseView, MinhaColecaoView

# Estas são as URLs que NÃO são gerenciadas pelo router do DRF
urlpatterns = [
    path('posses/adicionar/', AdicionarPosseView.as_view(), name='adicionar-posse'),
    path('colecoes/minha-colecao/', MinhaColecaoView.as_view(), name='minha-colecao'),
]
