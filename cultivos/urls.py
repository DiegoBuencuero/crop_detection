from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalisisImagenViewSet, TipoCultivoViewSet, RegistroAnalisisViewSet, index

router = DefaultRouter()
router.register(r'analisis', AnalisisImagenViewSet, basename='analisis')
router.register(r'tipos-cultivo', TipoCultivoViewSet, basename='tipo-cultivo')
router.register(r'registros', RegistroAnalisisViewSet, basename='registro')

urlpatterns = [
    path('', include(router.urls)),
]
