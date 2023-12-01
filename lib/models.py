from django.db import models
from django.utils import timezone

# Create your models here.

class Vuelo(models.Model):
    id= models.AutoField(primary_key=True)
    origen= models.CharField(max_length=100, verbose_name='Origen')
    destino= models.CharField(max_length=100, verbose_name='Destino')
    horasalida= models.DateTimeField(verbose_name='Salida')
    Escalado= models.BooleanField(verbose_name='Escalas')

    def __str__(self):
        return  self.origen + "-" + self.destino #+ #" " + str(self.horasalida.hour()
    


    