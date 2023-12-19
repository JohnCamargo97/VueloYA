from django.db import models


class user(models.Model):
    email = models.EmailField(verbose_name='user email')
    fullname= models.CharField(max_length=100, verbose_name='full name')
    password= models.CharField(max_length=50)


    def __str__(self):
        return  self.fullname