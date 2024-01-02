from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
class aerolinea(models.Model):
    #id = models.IntegerField(primary_key=True)
    nombre_aerolinea= models.CharField(max_length=100, verbose_name='nombre')
    logo_aerolinea = models.ImageField(upload_to="logos_aerolineas")

    def __str__(self):
        return self.nombre_aerolinea

class Vuelo(models.Model):
    #id= models.AutoField(primary_key=True)
    origen= models.CharField(max_length=100, verbose_name='Origen')
    destino= models.CharField(max_length=100, verbose_name='Destino')
    
    fechasalida= models.DateField(verbose_name='fecha salida', blank=True)
    horasalida1= models.TimeField(verbose_name='hora salida', blank=True, default=None)
    horasalida2= models.TimeField(verbose_name='hora llegada', blank=True, default=None)
    
    fechavuelta= models.DateField(verbose_name='fecha regreso', blank=True)
    horavuelta1= models.TimeField(verbose_name='hora salida', blank=True, default=None)
    horavuelta2= models.TimeField(verbose_name='hora llegada', blank=True, default=None)
    
    id_aerolinea= models.ForeignKey(aerolinea, on_delete=models.CASCADE)
    Escalado= models.BooleanField(verbose_name='Escalas')
    escalas= models.IntegerField(verbose_name='# escalas', blank=True, default= 0)
    precio= models.CharField(max_length=100, verbose_name='Precio', default= 'ND')
    Ida_vuelta= models.BooleanField(default=False, verbose_name='ida_vuelta')

    def __str__(self):
        idstr= str(self.id)
        return  idstr + "-" +self.origen + "-" + self.destino #+ #" " + str(self.horasalida.hour()
    
class puestos(models.Model):
    #id = models.IntegerField(primary_key=True)
    Vuelo_id= models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    numero= models.IntegerField(verbose_name='puesto')
    Ejecutivo_bool= models.BooleanField(verbose_name='Ejecutivo o comercial')    
    Ventana_bool= models.BooleanField(verbose_name='Ventana o pasillo')

    def __str__(self):
        numerostr = str(self.id)
        return  numerostr
    

class userVueloYa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='default.png', upload_to='profile_pictures')

    def __str__(self):
            return f'{self.user.username}'
    
    #overrite save function for the model to resize images
    def save(self):
        #run the father class first
        super().save()

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
