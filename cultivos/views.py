from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import AnalisisImagenForm
from .models import AnalisisImagen, TipoCultivo, RegistroAnalisis
from ml_modules.processors import procesar_imagen_cultivos


def index(request):
    return render(request, 'index.html')


@login_required
def analizar_imagen(request):
    """Vista para upload y análisis de imagen"""

    if request.method == 'POST':
        form = AnalisisImagenForm(request.POST, request.FILES)

        if form.is_valid():
            analisis = form.save(commit=False)
            analisis.estado = 'procesando'
            analisis.save()

            try:
                ruta_imagen = analisis.imagen.path
                resultado = procesar_imagen_cultivos(ruta_imagen)

                cultivo = TipoCultivo.objects.filter(
                    codigo=resultado['cultivo']
                ).first()

                analisis.tipo_cultivo = cultivo
                analisis.confianza = resultado['confianza']
                analisis.cantidad_plantas = resultado['cantidad_plantas']
                analisis.estado = 'completado'
                analisis.fecha_procesamiento = timezone.now()
                analisis.datos_json = resultado
                analisis.save()

                messages.success(request, 'Análisis completado correctamente')
                return redirect('resultado', id=analisis.id)

            except Exception as e:
                analisis.estado = 'error'
                analisis.datos_json = {'error': str(e)}
                analisis.save()
                messages.error(request, f'Error al procesar: {str(e)}')

    else:
        form = AnalisisImagenForm()

    return render(request, 'analizar.html', {'form': form})


def resultado(request, id):
    """Muestra resultado del análisis"""
    try:
        analisis = AnalisisImagen.objects.get(id=id)
    except:
        return redirect('analizar_imagen')

    return render(request, 'resultado.html', {'analisis': analisis})


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
