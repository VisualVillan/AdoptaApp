from django import forms
from datetime import date
from .models import TipoMascota, Mascota, Persona, PostMascota


class TipoMascotaForm(forms.ModelForm):
    class Meta:
        model = TipoMascota
        fields = ['nombre', 'descripcion']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Perro'
            }),
            'descripcion': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Ej. Mascotas caninas de todas las razas',
                'rows':3
            }) 
        }

        labels = {
            'nombre':'Nombre del tipo',
            'descripcion': 'Descripcion'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or nombre.strip() == '':
            raise forms.ValidationError("El nombre no puede estar vacio")
        if TipoMascota.objects.filter(nombre__iexact=nombre.strip()).exists():
            raise forms.ValidationError("Este tipo de mascota ya existe")
        return nombre.strip()
    
    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        descripcion = cleaned.get('descripcion')
        if nombre and descripcion and nombre.strip().lower() == descripcion.strip().lower():
            raise forms.ValidationError("El nombre y la descripcion no pueden ser iguales")
        return cleaned
    
class PostMascotaForm(forms.ModelForm):
    class Meta:
        model = PostMascota
        fields = ['titulo', 'descripcion', 'fecha', 'foto']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Primer paseo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe el momento (mínimo 20 caracteres)',
                'rows': 4
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'fecha': 'Fecha',
            'foto': 'Foto',
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')
        if len(descripcion.strip()) < 20:
            raise forms.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return descripcion

    def clean_fecha(self):
        f = self.cleaned_data.get('fecha')
        if f and f > date.today():
            raise forms.ValidationError("La fecha no puede ser mayor a la actual.")
        return f
