from django.urls import path
from .views import index, analizar_imagen, resultado

urlpatterns = [
    path('', index, name='index'),
    path('analizar/', analizar_imagen, name='analizar_imagen'),
    path('resultado/<int:id>/', resultado, name='resultado'),
]
