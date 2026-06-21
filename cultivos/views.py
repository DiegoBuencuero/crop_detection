from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render
from .models import AnalisisImagen, TipoCultivo, RegistroAnalisis
from .serializers import AnalisisImagenSerializer, TipoCultivoSerializer, RegistroAnalisisSerializer
from ml_modules.processors import procesar_imagen_cultivos


def index(request):
    return render(request, 'index.html')


class TipoCultivoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoCultivo.objects.all()
    serializer_class = TipoCultivoSerializer
    filterset_fields = ['nombre', 'codigo']


class AnalisisImagenViewSet(viewsets.ModelViewSet):
    queryset = AnalisisImagen.objects.all()
    serializer_class = AnalisisImagenSerializer

    def create(self, request, *args, **kwargs):
        """Sube imagen y dispara análisis"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        analisis = serializer.save(estado='procesando')

        try:
            resultado = procesar_imagen_cultivos(analisis.imagen.path)

            tipo_cultivo = TipoCultivo.objects.filter(
                codigo=resultado['cultivo']
            ).first()

            analisis.tipo_cultivo = tipo_cultivo
            analisis.confianza = resultado['confianza']
            analisis.cantidad_plantas = resultado['cantidad_plantas']
            analisis.estado = 'completado'
            analisis.fecha_procesamiento = timezone.now()
            analisis.datos_json = resultado
            analisis.save()

            return Response(
                AnalisisImagenSerializer(analisis).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            analisis.estado = 'error'
            analisis.datos_json = {'error': str(e)}
            analisis.save()
            return Response(
                {
                    'id': analisis.id,
                    'estado': 'error',
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def resultados(self, request, pk=None):
        """Obtiene resultados detallados del análisis"""
        analisis = self.get_object()
        return Response({
            'id': analisis.id,
            'estado': analisis.estado,
            'cultivo': analisis.tipo_cultivo.nombre if analisis.tipo_cultivo else None,
            'confianza': f"{analisis.confianza:.2f}%",
            'cantidad_plantas': analisis.cantidad_plantas,
            'fecha_carga': analisis.fecha_carga.isoformat(),
            'fecha_procesamiento': analisis.fecha_procesamiento.isoformat() if analisis.fecha_procesamiento else None,
        })


class RegistroAnalisisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroAnalisis.objects.all()
    serializer_class = RegistroAnalisisSerializer
    filterset_fields = ['usuario', 'analisis']
