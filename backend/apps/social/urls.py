from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.programas import EstadoProgramaViewSet, ProgramaSocialViewSet
from .views.beneficiarios import (
    ProgramaBeneficiarioViewSet,
    ActividadSocialViewSet,
    CoberturaProgramaViewSet
)
from .views.autoridades import (
    TipoAutoridadViewSet,
    RolAutoridadViewSet,
    AutoridadComunitariaViewSet
)
from .views.actividades import (
    TipoActividadViewSet,
    EstadoActividadViewSet,
    ActividadComunitariaViewSet,
    AsistenciaActividadViewSet
)

# Configuración del router para las vistas del módulo social
router = DefaultRouter()
router.register(r'estados', EstadoProgramaViewSet, basename='estado')
router.register(r'programas', ProgramaSocialViewSet, basename='programa')
router.register(r'beneficiarios', ProgramaBeneficiarioViewSet, basename='beneficiario')
router.register(r'actividades', ActividadSocialViewSet, basename='actividad')
router.register(r'coberturas', CoberturaProgramaViewSet, basename='cobertura')
router.register(r'tipos-autoridad', TipoAutoridadViewSet, basename='tipo_autoridad')
router.register(r'roles-autoridad', RolAutoridadViewSet, basename='rol_autoridad')
router.register(r'autoridades', AutoridadComunitariaViewSet, basename='autoridad')
router.register(r'tipos-actividad', TipoActividadViewSet, basename='tipo_actividad')
router.register(r'estados-actividad', EstadoActividadViewSet, basename='estado_actividad')
router.register(r'actividades-comunitarias', ActividadComunitariaViewSet, basename='actividad_comunitaria')
router.register(r'asistencias-actividad', AsistenciaActividadViewSet, basename='asistencia_actividad')

# Definición de las URLs del módulo social con namespace
urlpatterns = [
    path('', include((router.urls, 'social'), namespace='social'))
]
