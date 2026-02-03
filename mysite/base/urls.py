from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

# Importando as views diretamente
from mercadosorcery import views as mercadosorcery_views
from socialentities import views as socialentities_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https"]
        return schema

schema_view = get_schema_view(
   openapi.Info(
      title="My Project API",
      default_version='v1',
      description="API documentation for My Project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myproject.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   generator_class=BothHttpAndHttpsSchemaGenerator
)

# As rotas gerenciadas pelo router padrão do DRF
router = routers.DefaultRouter()
router.register(r'users', socialentities_views.SocialEntityViewSet, basename='socialentity')
router.register(r'cartas', mercadosorcery_views.CartaViewSet)
router.register(r'colecoes', mercadosorcery_views.ColecaoViewSet)
router.register(r'posses', mercadosorcery_views.PosseViewSet)
router.register(r'listas', mercadosorcery_views.ListaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas de documentação da API
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/?$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/?$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # --- ROTAS DA API ---

    # Rotas personalizadas
    path('api/posses/adicionar/', mercadosorcery_views.AdicionarPosseView.as_view(), name='adicionar-posse'),
    path('api/colecoes/minha-colecao/', mercadosorcery_views.MinhaColecaoView.as_view(), name='minha-colecao'),

    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rotas do DRF Router (deve ser a última rota da API)
    path('api/', include(router.urls)),
]
