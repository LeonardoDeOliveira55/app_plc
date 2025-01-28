from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.empresa_id:
            self.fields['ubicacion'].queryset = Sector.objects.filter(empresa=self.instance.empresa)
        elif self.data.get('empresa'):
            self.fields['ubicacion'].queryset = Sector.objects.filter(empresa=self.data.get('empresa'))
        else:
            self.fields['ubicacion'].queryset = Sector.objects.none()

    class Meta:
        model = Tag
        fields = ['nombre', 'descripcion', 'empresa', 'ubicacion']

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['tipo_io', 'direccion_plc', 'slot', 'bastidor', 'direccion', 'numero_modulo', 'numero_entrada']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']        


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre']

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['empresa', 'sector', 'ubicacion']
        


###########################################################################################################

        
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description']

class ContactorConfigForm(forms.Form):
    number_of_contactors = forms.IntegerField(
        min_value=1,
        max_value=14,
        label="Número de contactores",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class CapacitorConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kvar_choices = kwargs.pop('kvar_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['kvar_values'] = forms.MultipleChoiceField(
            choices=kvar_choices,
            label="Baterías conectadas",
            help_text="Seleccione las baterías conectadas a este contactor (máximo 3)",
            widget=forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '4'  # Muestra 4 opciones sin necesidad de scroll
            })
        )

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['current_r', 'current_s', 'current_t', 'notes']
        widgets = {
            'current_r': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_s': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_t': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }