from rest_framework import serializers
from .models import AnalisisImagen, TipoCultivo, RegistroAnalisis


class TipoCultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCultivo
        fields = ['id', 'nombre', 'codigo', 'descripcion']


class AnalisisImagenSerializer(serializers.ModelSerializer):
    tipo_cultivo = TipoCultivoSerializer(read_only=True)
    tipo_cultivo_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = AnalisisImagen
        fields = [
            'id', 'imagen', 'tipo_cultivo', 'tipo_cultivo_id',
            'confianza', 'cantidad_plantas', 'estado',
            'fecha_carga', 'fecha_procesamiento', 'imagen_procesada',
            'datos_json'
        ]
        read_only_fields = [
            'tipo_cultivo', 'confianza', 'cantidad_plantas',
            'estado', 'imagen_procesada', 'datos_json',
            'fecha_carga', 'fecha_procesamiento'
        ]


class RegistroAnalisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAnalisis
        fields = ['id', 'analisis', 'usuario', 'fecha', 'ip_address', 'notas']
        read_only_fields = ['fecha']
