from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('busqueda', views.busqueda, name='busqueda'),
    path('home_dev2', views.home_dev2, name='home_dev2'),
    path('misviajes', views.misviajes, name='misviajes'),
    path('iniciarsesion', views.iniciarsesion, name='iniciarsesion'),
    path('registrarse', views.registrarse, name='registrarse'),
    path('resultados', views.resultados, name='resultados'),
]