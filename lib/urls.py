from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from users import views as users_views

urlpatterns = [
    path('home', views.home, name='home'),
    path('busqueda', views.busqueda, name='busqueda'),
    path('misviajes', views.misviajes, name='misviajes'),
    path('pagos', views.pagos, name='pagos'),
    path('resultados', views.resultados, name='resultados'),
    path('resumen', views.resumen, name='resumen'),

    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
] +  static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)