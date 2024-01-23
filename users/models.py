from django.db import models
from django.contrib.auth.models import User
from lib.models import puestos

class userFacturacion(models.Model):
    SITUACION_FISCAL = [
         ("Persona Natural", "Persona Natural"),
         ("Persona Juridica", "Persona Juridica")
    ]
    TIPO_DOCUMENTO = [
         ("CC", "CC"),
         ("TI", "TI"),
         ("Pasaporte", "Pasaporte")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    situacionFiscal = models.CharField(max_length= 40, choices=SITUACION_FISCAL)
    nombre = models.CharField(max_length= 40)
    apellido = models.CharField(max_length= 40)
    tipoDeDocumento = models.CharField(max_length= 40, choices=TIPO_DOCUMENTO)
    nDocumento = models.IntegerField()
    departamento = models.CharField(max_length= 40)
    ciudad = models.CharField(max_length= 40)
    direccion = models.CharField(max_length= 40)

    def __str__(self):
            return f'{self.nombre} {self.apellido} {self.tipoDeDocumento} {self.nDocumento}'

class pasajero(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    puesto = models.OneToOneField(puestos, default=200, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length= 40)
    apellido = models.CharField(max_length= 40)
    tipoDeDocumento = models.CharField(max_length= 40)
    nDocumento = models.IntegerField()
    ciudadDeResidencia = models.CharField(max_length= 40)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'