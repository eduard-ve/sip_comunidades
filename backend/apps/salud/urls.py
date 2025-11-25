from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistroSaludViewSet, AlertaSaludViewSet, ControlSaludViewSet, SaludStatsViewSet,
    HistorialMedicoViewSet, VacunaViewSet, MedicamentoViewSet, ExamenMedicoViewSet
)

router = DefaultRouter()
router.register(r'registros', RegistroSaludViewSet, basename='registros-salud')
router.register(r'alertas', AlertaSaludViewSet, basename='alertas-salud')
router.register(r'controles', ControlSaludViewSet, basename='controles-salud')
router.register(r'stats', SaludStatsViewSet, basename='salud-stats')
router.register(r'historiales', HistorialMedicoViewSet, basename='historiales-medicos')
router.register(r'vacunas', VacunaViewSet, basename='vacunas')
router.register(r'medicamentos', MedicamentoViewSet, basename='medicamentos')
router.register(r'examenes', ExamenMedicoViewSet, basename='examenes-medicos')

urlpatterns = [
    path('', include(router.urls)),
]