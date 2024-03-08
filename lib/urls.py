from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from users import views as users_views


urlpatterns = [
    path('home', views.home, name='home'),
    path('busqueda/<str:origen>/<str:destino>/<int:pas>/', views.resultado.as_view(), name='busqueda'),
    path('misviajes', views.misviajes, name='misviajes'),
    path('misviajes/borrar/<int:pk>', views.viajes_borrar, name='viajes_borrar'),
    path('pagos/<int:pk>', views.pagos, name='pagos'),
    path('resumen', views.resumen, name='resumen'),
    path('footer', views.footer, name='footer'),

    path('users/', include('users.urls')),
    #path('users/', include('django.contrib.auth.urls')),
] +  static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)