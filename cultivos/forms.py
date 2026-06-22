from django import forms
from django.forms import ModelForm
from .models import AnalisisImagen


class BaseForm(ModelForm):
    """Clase base para todos los forms - añade form-control automáticamente"""
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AnalisisImagenForm(BaseForm):
    """Form para upload de imágenes - misma estructura que CampoForm de new_agro"""
    class Meta:
        model = AnalisisImagen
        fields = ["imagen"]
        widgets = {
            "imagen": forms.FileInput(attrs={
                "accept": "image/*",
                "class": "form-control"
            })
        }
