# apps/encuestas/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EncuestaViewSet, PreguntaViewSet, OpcionViewSet, RespuestaViewSet

app_name = 'encuestas'

# Configuración del enrutador para las vistas de encuestas
router = DefaultRouter()
router.register(r'', EncuestaViewSet, basename='encuestas')
router.register(r'preguntas', PreguntaViewSet, basename='preguntas')
router.register(r'opciones', OpcionViewSet, basename='opciones')
router.register(r'respuestas', RespuestaViewSet, basename='respuestas')

urlpatterns = router.urls
