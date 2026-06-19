from django.db import models
from django.utils import timezone


class TipoCultivo(models.Model):
    """Tipos de cultivos disponibles"""
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipo de Cultivo"
        verbose_name_plural = "Tipos de Cultivos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class AnalisisImagen(models.Model):
    """Análisis de imágenes de cultivos"""
    ESTADO_CHOICES = [
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('error', 'Error'),
    ]

    imagen = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    tipo_cultivo = models.ForeignKey(
        TipoCultivo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de cultivo identificado"
    )
    confianza = models.FloatField(
        default=0.0,
        help_text="Porcentaje de confianza en la identificación (0-100)"
    )
    cantidad_plantas = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Cantidad de plantas detectadas"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='procesando'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True)
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    imagen_procesada = models.ImageField(
        upload_to='processed/%Y/%m/%d/',
        blank=True,
        help_text="Imagen con detecciones dibujadas"
    )
    datos_json = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Datos adicionales del análisis"
    )

    class Meta:
        ordering = ['-fecha_carga']
        verbose_name = "Análisis de Imagen"
        verbose_name_plural = "Análisis de Imágenes"

    def __str__(self):
        return f"Análisis #{self.id} - {self.tipo_cultivo or 'Sin identificar'}"


class RegistroAnalisis(models.Model):
    """Historial de análisis realizados"""
    analisis = models.ForeignKey(AnalisisImagen, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Registro de Análisis"
        verbose_name_plural = "Registros de Análisis"
        ordering = ['-fecha']

    def __str__(self):
        return f"Registro {self.id} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
