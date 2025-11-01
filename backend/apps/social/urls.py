from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.programas import EstadoProgramaViewSet, ProgramaSocialViewSet
from .views.beneficiarios import (
    ProgramaBeneficiarioViewSet,
    ActividadSocialViewSet,
    CoberturaProgramaViewSet
)

# Configuración del router para las vistas del módulo social
router = DefaultRouter()
router.register(r'estados', EstadoProgramaViewSet, basename='estado')
router.register(r'programas', ProgramaSocialViewSet, basename='programa')
router.register(r'beneficiarios', ProgramaBeneficiarioViewSet, basename='beneficiario')
router.register(r'actividades', ActividadSocialViewSet, basename='actividad')
router.register(r'coberturas', CoberturaProgramaViewSet, basename='cobertura')

# Definición de las URLs del módulo social con namespace
urlpatterns = [
    path('', include((router.urls, 'social'), namespace='social'))
]
