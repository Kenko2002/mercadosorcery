from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocialEntityViewSet, LoginView, MeView

router = DefaultRouter()
router.register(r'users', SocialEntityViewSet, basename='socialentity')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
]
