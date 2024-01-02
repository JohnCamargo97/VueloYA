from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from lib.models import userVueloYa

@receiver(post_save, sender=User)
def create_UserVueloYa(sender, instance, created, **kwargs):
    if created:
        userVueloYa.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_UserVueloYa(sender, instance, **kwargs):
    instance.uservueloya.save()
