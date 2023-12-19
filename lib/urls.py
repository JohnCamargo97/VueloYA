from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from users import views as users_views

urlpatterns = [
    path('home', views.home, name='home'),
    path('busqueda', views.busqueda, name='busqueda'),
    path('home_dev2', views.home_dev2, name='home_dev2'),
    path('misviajes', views.misviajes, name='misviajes'),
    path('registrarse', views.registrarse, name='registrarse'),
    path('resultados', views.resultados, name='resultados'),

    path('users/', include('django.contrib.auth.urls')),
    path('register', users_views.register, name='register'),
    path('login', users_views.login_user, name='login'),
    path('mensaje_user', users_views.mensaje_user, name='mensaje_user'),
] +  static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)