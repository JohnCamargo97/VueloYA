from django import forms
from .models import user

class formUser(forms.ModelForm):
   
   class Meta:
      model = user
      fields ='__all__'
    