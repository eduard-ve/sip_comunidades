from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.programas import EstadoProgramaViewSet, ProgramaSocialViewSet
from .views.beneficiarios import ProgramaBeneficiarioViewSet, ActividadSocialViewSet, CoberturaProgramaViewSet

# Configuración del router para las vistas del módulo social
router = DefaultRouter()
router.register(r'estados', EstadoProgramaViewSet, basename='estados')
router.register(r'programas', ProgramaSocialViewSet, basename='programas')
router.register(r'beneficiarios', ProgramaBeneficiarioViewSet, basename='beneficiarios')
router.register(r'actividades', ActividadSocialViewSet, basename='actividades')
router.register(r'coberturas', CoberturaProgramaViewSet, basename='coberturas')

# Definición de las URLs del módulo social
urlpatterns = router.urls
