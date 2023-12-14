from django.db import models
from django.utils import timezone

# Create your models here.

class Vuelo(models.Model):
    #id= models.AutoField(primary_key=True)
    origen= models.CharField(max_length=100, verbose_name='Origen')
    destino= models.CharField(max_length=100, verbose_name='Destino')
    fechasalida= models.DateTimeField(default='2023-12-01 00:00:00', verbose_name='Salida_d', blank=True)
    fechavuelta= models.DateTimeField(default='2023-12-01 00:00:00', verbose_name='vuelta_d', blank=True)
    Escalado= models.BooleanField(verbose_name='Escalas')
    Ida_vuelta= models.BooleanField(default=False, verbose_name='ida_vuelta')

    def __str__(self):
        idstr= str(self.id)
        return  idstr + "-" +self.origen + "-" + self.destino #+ #" " + str(self.horasalida.hour()
    
class puestos(models.Model):
    id = models.IntegerField(primary_key=True)
    Vuelo_id= models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    numero= models.IntegerField(verbose_name='puesto')
    Ejecutivo_bool= models.BooleanField(verbose_name='Ejecutivo o comercial')    
    Ventana_bool= models.BooleanField(verbose_name='Ventana o pasillo')

    def __str__(self):
        numerostr = str(self.id)
        return  numerostr

class usuarios(models.Model):
    email = models.EmailField(verbose_name='user email')
    FullName= models.CharField(max_length=100, verbose_name='full name')

    def __str__(self):
        return  self.FullName


    