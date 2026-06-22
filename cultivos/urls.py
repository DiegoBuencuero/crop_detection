from django.urls import path
from .views import index, analizar_imagen, resultado, laboratorio_hsv

urlpatterns = [
    path('', index, name='index'),
    path('analizar/', analizar_imagen, name='analizar_imagen'),
    path('resultado/<int:id>/', resultado, name='resultado'),
    path('laboratorio/', laboratorio_hsv, name='laboratorio_hsv'),
]
