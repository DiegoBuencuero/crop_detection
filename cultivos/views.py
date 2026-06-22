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


def laboratorio_hsv(request):
    """Laboratorio para ajustar rangos HSV de cultivos"""
    import cv2
    import numpy as np
    import json
    from base64 import b64encode

    datos = {
        'imagen_base64': None,
        'estadisticas': None,
        'rango_sugerido': None,
        'error': None
    }

    if request.method == 'POST' and request.FILES.get('imagen'):
        try:
            archivo = request.FILES['imagen']
            contenido = archivo.read()

            # Cargar imagen
            nparr = np.frombuffer(contenido, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                datos['error'] = 'No se pudo cargar la imagen'
                return render(request, 'laboratorio_hsv.html', datos)

            # Convertir a HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h = hsv[:, :, 0]
            s = hsv[:, :, 1]
            v = hsv[:, :, 2]

            # Estadísticas
            stats = {
                'hue': {
                    'min': int(h.min()),
                    'max': int(h.max()),
                    'promedio': float(h.mean()),
                    'desv_est': float(h.std()),
                    'p10': int(np.percentile(h, 10)),
                    'p25': int(np.percentile(h, 25)),
                    'p50': int(np.percentile(h, 50)),
                    'p75': int(np.percentile(h, 75)),
                    'p90': int(np.percentile(h, 90)),
                },
                'saturation': {
                    'min': int(s.min()),
                    'max': int(s.max()),
                    'promedio': float(s.mean()),
                    'desv_est': float(s.std()),
                    'p10': int(np.percentile(s, 10)),
                    'p25': int(np.percentile(s, 25)),
                    'p50': int(np.percentile(s, 50)),
                    'p75': int(np.percentile(s, 75)),
                    'p90': int(np.percentile(s, 90)),
                },
                'value': {
                    'min': int(v.min()),
                    'max': int(v.max()),
                    'promedio': float(v.mean()),
                    'desv_est': float(v.std()),
                    'p10': int(np.percentile(v, 10)),
                    'p25': int(np.percentile(v, 25)),
                    'p50': int(np.percentile(v, 50)),
                    'p75': int(np.percentile(v, 75)),
                    'p90': int(np.percentile(v, 90)),
                }
            }

            # Rango sugerido
            h_sorted = np.sort(h.flatten())
            s_sorted = np.sort(s.flatten())
            v_sorted = np.sort(v.flatten())

            rango = {
                'lower': [
                    max(0, int(np.percentile(h_sorted, 10))),
                    max(0, int(np.percentile(s_sorted, 10))),
                    max(0, int(np.percentile(v_sorted, 10))),
                ],
                'upper': [
                    min(180, int(np.percentile(h_sorted, 90))),
                    255,
                    255
                ]
            }

            # Codificar imagen a base64 para mostrar
            _, buffer = cv2.imencode('.jpg', img)
            img_base64 = b64encode(buffer).decode()

            datos['imagen_base64'] = img_base64
            datos['estadisticas'] = stats
            datos['rango_sugerido'] = rango

        except Exception as e:
            datos['error'] = f'Error: {str(e)}'

    return render(request, 'laboratorio_hsv.html', datos)
