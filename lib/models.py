import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

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
    precio= models.IntegerField(verbose_name='Precio', default= 0)
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

class userVueloYa(models.Model):

    GENEROS=[
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Prefiero no decir", "Prefiero no decir")       
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='profile_pictures/default.png', upload_to= 'profile_pictures', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    genero = models.CharField(default='No especificado', max_length=25, choices=GENEROS)
    fechaNacimiento = models.DateField(default='1900-01-01', blank=True)
    telefono = models.CharField(default='', blank=True, max_length=10)

    def __str__(self):
            return f'{self.user.username}'
    
    #rename picture to upload
    def wrapper(instance, filename):
        extension= filename.split('.')[-1]
        print(extension)
        if instance.pk:
            filename= '{}{}'.format(instance.user.username, extension)
        else:
            # set filename as random string
            filename  = '{}.{}'.format(uuid4().hex, extension)
        # return the whole path to the file
        return os.path.join(path, filename)

    #overrite save function for the model to resize images and replace old ones
    def save(self, *args, **kwargs):
        #run the father class first deleting old picture
        try:
            actual= userVueloYa.objects.get(id=self.id)
            if actual.picture!= self.picture:
                actual.picture.delete(save=False)
                #create thumbnail 1:1 aspect ratio if picture exists and not repeated
                try:
                    img = Image.open(self.picture.path)

                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                    w, h = img.size
                    if w > h:
                        (left, upper, right, lower) = ((w-h)/2, 0, h+(w-h)/2, h)
                    else:
                        (left, upper, right, lower) = (0, (h-w)/2, w, w+(h-w)/2)
                    img.crop((left, upper, right, lower)).save(self.picture.path)
                except:
                    pass
                print("picture deleted")              
        except ObjectDoesNotExist:
            pass
        super().save(*args, **kwargs)

class historicoReserva(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    vuelo = models.ForeignKey(Vuelo, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    duracion = models.DurationField(verbose_name='total', default= timedelta(days=1))
    puestos = models.CharField(max_length=25)
    pasajeros = models.SmallIntegerField()
    total= models.IntegerField(verbose_name='total', default= 6500000)
    estado = models.CharField(max_length=25)
    
class oferta(models.Model):
    vuelo = models.OneToOneField(Vuelo, on_delete=models.DO_NOTHING)
    image = models.ImageField(default='defaultbg.jpg', upload_to= 'imagen_ofertas')
    descripcion = models.TextField()

    def __str__(self):
        return f'{self.vuelo.origen} - {self.vuelo.destino}'


class lugarTuristico(models.Model):
    vuelo = models.ForeignKey(Vuelo, on_delete=models.DO_NOTHING)
    nombre_lugar= models.CharField(max_length=100, verbose_name='nombre')
    image = models.ImageField(default='defaultbg.jpg', upload_to= 'imagen_ofertas')
    descripcion = models.TextField()

    def __str__(self):
        return f'{self.nombre_lugar}'
