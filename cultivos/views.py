from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import AnalisisImagenForm
from .models import AnalisisImagen, TipoCultivo
from ml_modules.processors import procesar_imagen_cultivos


def index(request):
    return render(request, 'index.html')


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
