from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroSaludViewSet, AlertaSaludViewSet, ControlSaludViewSet

router = DefaultRouter()
router.register(r'registros', RegistroSaludViewSet, basename='registros-salud')
router.register(r'alertas', AlertaSaludViewSet, basename='alertas-salud')
router.register(r'controles', ControlSaludViewSet, basename='controles-salud')

urlpatterns = [
    path('', include(router.urls)),
]