from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import userFacturacion, pasajero, puestos

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

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      for visible in self.visible_fields():
         visible.field.widget.attrs['class'] = 'input-datos-facturacion'
         visible.field.widget.attrs['placeholder'] = visible.field.label
      
      self.fields["situacionFiscal"].widget.attrs.update({"class": "select-tipo-documento-situacion-fiscal"})
      self.fields["tipoDeDocumento"].widget.attrs.update({"class": "select-tipo-documento-situacion-fiscal"})
      
   class Meta:
      model = userFacturacion
      fields = ('situacionFiscal', 'nombre', 'apellido', 'tipoDeDocumento', 'nDocumento', 'departamento', 'ciudad', 'direccion')

class userPasajeroForm(forms.ModelForm):
   
   PUESTOS = puestos.objects.all().values_list('id', 'id')
   puesto = forms.ChoiceField(widget=forms.Select, choices=PUESTOS)
   
   TIPO_DOCUMENTO = [
        ("cedula", "Cedula"),
        ("tarjeta-identidad", "Tarjeta de Identidad"),
        ("pasaporte", "Pasaporte"),
    ]
   tipoDeDocumento = forms.ChoiceField(widget=forms.Select, choices=TIPO_DOCUMENTO)

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields["nombre"].widget.attrs.update({"class": "cotenedor-imput-viajeros"})
      self.fields["apellido"].widget.attrs.update({"class": "cotenedor-imput-viajeros"})
      self.fields["tipoDeDocumento"].widget.attrs.update({"class": "contenedor-select-viajeros"})
      self.fields["nDocumento"].widget.attrs.update({"class": "cotenedor-imput-viajeros"})
      self.fields["ciudadDeResidencia"].widget.attrs.update({"class": "cotenedor-imput-viajeros"})
      self.fields["puesto"].widget.attrs.update({"class": "contenedor-select-viajeros"})

   class Meta:
      model = pasajero
      fields = ('puesto', 'nombre', 'apellido', 'tipoDeDocumento', 'nDocumento', 'ciudadDeResidencia')
      
