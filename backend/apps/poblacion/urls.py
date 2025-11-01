from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.poblacion.views.personas import PersonaViewSet
from apps.poblacion.views.relaciones import RelacionFamiliarViewSet
from apps.poblacion.serializers.catalogos import CatalogoViewSet
from apps.poblacion.views.stats import population_stats

router = DefaultRouter()

# Catalogos solo lectura
router.register(r'tipos_identificacion', CatalogoViewSet, basename='tipos_identificacion')
router.register(r'niveles_educativos', CatalogoViewSet, basename='niveles_educativos')
router.register(r'ocupaciones', CatalogoViewSet, basename='ocupaciones')
router.register(r'grupos_familiares', CatalogoViewSet, basename='grupos_familiares')
router.register(r'estados_civiles', CatalogoViewSet, basename='estados_civiles')
router.register(r'lenguas', CatalogoViewSet, basename='lenguas')
router.register(r'tipos_relaciones', CatalogoViewSet, basename='tipos_relaciones')

# CRUD principal para personas
router.register(r'personas', PersonaViewSet)
router.register(r'relaciones_familiares', RelacionFamiliarViewSet)

# Endpoint adicional para estadísticas
urlpatterns = [
    path('stats/', population_stats, name='population_stats'),
] + router.urls