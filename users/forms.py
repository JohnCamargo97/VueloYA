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

   puesto = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PUESTOS)

   class Meta:
      model = pasajero
      fields = ('puesto', 'nombre', 'apellido', 'tipoDeDocumento', 'nDocumento', 'ciudadDeResidencia')
      
