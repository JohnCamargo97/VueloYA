from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('misviajes', views.misviajes, name='misviajes'),
    path('iniciarsesion', views.iniciarsesion, name='iniciarsesion'),
    path('registrarse', views.registrarse, name='registrarse'),
]