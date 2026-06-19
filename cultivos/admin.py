from django.contrib import admin
from .models import TipoCultivo, AnalisisImagen, RegistroAnalisis


@admin.register(TipoCultivo)
class TipoCultivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'descripcion']
    search_fields = ['nombre', 'codigo']
    list_filter = ['nombre']


@admin.register(AnalisisImagen)
class AnalisisImagenAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_cultivo', 'confianza', 'cantidad_plantas', 'estado', 'fecha_carga']
    search_fields = ['id', 'tipo_cultivo__nombre']
    list_filter = ['estado', 'fecha_carga', 'tipo_cultivo']
    readonly_fields = ['fecha_carga', 'fecha_procesamiento', 'estado', 'confianza', 'cantidad_plantas']

    fieldsets = (
        ('Imagen', {'fields': ('imagen', 'imagen_procesada')}),
        ('Resultados', {'fields': ('tipo_cultivo', 'confianza', 'cantidad_plantas')}),
        ('Procesamiento', {'fields': ('estado', 'fecha_carga', 'fecha_procesamiento', 'datos_json')}),
    )


@admin.register(RegistroAnalisis)
class RegistroAnalisisAdmin(admin.ModelAdmin):
    list_display = ['id', 'analisis', 'usuario', 'fecha', 'ip_address']
    search_fields = ['usuario', 'analisis__id']
    list_filter = ['fecha', 'usuario']
    readonly_fields = ['fecha']
