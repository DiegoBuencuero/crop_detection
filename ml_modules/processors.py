"""
Módulo principal de procesamiento de imágenes de cultivos.
Detecta plantas y clasifica tipos de cultivo.
"""
import cv2
import numpy as np
from pathlib import Path


def procesar_imagen_cultivos(ruta_imagen):
    """
    Procesa imagen: identifica cultivo y cuenta plantas

    Args:
        ruta_imagen: ruta a la imagen

    Returns:
        dict con:
            - cultivo: código del cultivo identificado
            - confianza: % de confianza (0-100)
            - cantidad_plantas: número de plantas detectadas
            - coordenadas: lista de bounding boxes
    """
    img = cv2.imread(str(ruta_imagen))
    if img is None:
        raise ValueError("No se pudo leer la imagen")

    resultado_cultivo = _identificar_cultivo(img)
    cantidad_plantas = _contar_plantas(img)
    coordenadas = _detectar_plantas(img)

    return {
        'cultivo': resultado_cultivo['tipo'],
        'confianza': round(resultado_cultivo['confianza'], 2),
        'cantidad_plantas': cantidad_plantas,
        'coordenadas': coordenadas,
        'metadata': {
            'ancho': img.shape[1],
            'alto': img.shape[0],
            'canales': img.shape[2]
        }
    }


def _identificar_cultivo(imagen):
    """
    Identifica tipo de cultivo basado en análisis de color HSV.
    Usa rangos de color característicos.
    """
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    cultivos_colores = {
        'maiz': {'rango': ((20, 100, 100), (40, 255, 255)), 'confianza_base': 0.85},
        'trigo': {'rango': ((35, 80, 90), (55, 255, 255)), 'confianza_base': 0.80},
        'soja': {'rango': ((25, 100, 100), (45, 255, 255)), 'confianza_base': 0.75},
    }

    puntuaciones = {}
    for cultivo, config in cultivos_colores.items():
        lower = np.array(config['rango'][0])
        upper = np.array(config['rango'][1])
        mask = cv2.inRange(hsv, lower, upper)
        pixeles = cv2.countNonZero(mask)
        total_pixeles = imagen.shape[0] * imagen.shape[1]
        porcentaje = (pixeles / total_pixeles) * 100
        confianza = min(porcentaje / 30 * config['confianza_base'], 100)
        puntuaciones[cultivo] = confianza

    cultivo_identificado = max(puntuaciones, key=puntuaciones.get)
    return {
        'tipo': cultivo_identificado,
        'confianza': puntuaciones[cultivo_identificado],
        'todas_puntuaciones': puntuaciones
    }


def _detectar_plantas(imagen):
    """
    Detecta plantas individuales y retorna coordenadas de bounding boxes.
    Usa contornos y morfología.
    """
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    coordenadas = []
    for contorno in contours:
        area = cv2.contourArea(contorno)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contorno)
            coordenadas.append({
                'x': int(x),
                'y': int(y),
                'ancho': int(w),
                'alto': int(h),
                'area': int(area)
            })

    return coordenadas


def _contar_plantas(imagen):
    """
    Cuenta cantidad total de plantas en la imagen.
    """
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    plantas = [c for c in contours if cv2.contourArea(c) > 500]
    return len(plantas)
