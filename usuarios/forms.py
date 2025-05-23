from django import forms
from movilidad.models import Accidente

class AccidenteForm(forms.ModelForm):
    class Meta:
        model = Accidente
        fields = ['camara', 'fecha_hora', 'descripcion', 'vehiculos_involucrados', 'gravedad', 'latitud', 'altitud']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }