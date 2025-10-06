from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroView, CustomTokenObtainPairView, PerfilView, UsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]

urlpatterns += router.urls
