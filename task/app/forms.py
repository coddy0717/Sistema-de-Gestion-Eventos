from django import forms
from .models import Evento, Ubicacion

class EventoForm(forms.ModelForm):
    ubicacion_texto = forms.CharField(label="Ubicación", max_length=255)

    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'ubicacion_texto', 'imagen', 'capacidad']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'capacidad': forms.NumberInput(attrs={'type': 'number'}),
        }

    def save(self, commit=True):
        ubicacion_nombre = self.cleaned_data.pop('ubicacion_texto')
        ubicacion, _ = Ubicacion.objects.get_or_create(nombre=ubicacion_nombre)
        self.instance.ubicacion = ubicacion
        return super().save(commit=commit)
