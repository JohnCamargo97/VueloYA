from django.db import models
from django.contrib.auth.models import User

class userFacturacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    situacionFiscal = models.CharField(max_length= 40)
    nombre = models.CharField(max_length= 40)
    apellido = models.CharField(max_length= 40)
    tipoDeDocumento = models.CharField(max_length= 40)
    nDocumento = models.IntegerField()
    departamento = models.CharField(max_length= 40)
    ciudad = models.CharField(max_length= 40)
    direccion = models.CharField(max_length= 40)

    def __str__(self):
            return f'{self.nombre} {self.apellido} {self.tipoDeDocumento} {self.nDocumento}'

class pasajero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length= 40)
    apellido = models.CharField(max_length= 40)
    tipoDeDocumento = models.CharField(max_length= 40)
    nDocumento = models.IntegerField()
    ciudadDeResidencia = models.CharField(max_length= 40)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'