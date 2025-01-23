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