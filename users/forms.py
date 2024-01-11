from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import userFacturacion, pasajero

class RegUserForm(UserCreationForm):
   
   email = forms.EmailField()
   first_name = forms.CharField(max_length=30, required=None)
   last_name = forms.CharField(max_length=30, required=None)

   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UpdateUserForm(forms.ModelForm):
   email = forms.EmailField()
   first_name = forms.CharField(max_length=30, required=None)
   last_name = forms.CharField(max_length=30, required=None)
   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email')
   
class userFactForm(forms.ModelForm):
   class Meta:
      model = userFacturacion
      fields = ('situacionFiscal', 'nombre', 'apellido', 'tipoDeDocumento', 'nDocumento', 'departamento', 'ciudad', 'direccion')

class userPasajeroForm(forms.ModelForm):
   class Meta:
      model = pasajero
      fields = "__all__"