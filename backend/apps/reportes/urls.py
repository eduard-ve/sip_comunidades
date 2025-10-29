from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReporteSaludViewSet, ReporteSocialViewSet, ReporteEncuestasViewSet

router = DefaultRouter()
router.register(r'salud', ReporteSaludViewSet, basename='reportes-salud')
router.register(r'social', ReporteSocialViewSet, basename='reportes-social')
router.register(r'encuestas', ReporteEncuestasViewSet, basename='reportes-encuestas')

urlpatterns = [
    path('', include(router.urls)),
]