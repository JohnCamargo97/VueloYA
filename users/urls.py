from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('register', views.register, name='registrarse'),
    path('login', views.login_user, name='iniciarsesion'),
    path('logout', views.logout_user, name='cerrarsesion'),
    path('mensaje_user', views.mensaje_user, name='mensaje_user'),
]