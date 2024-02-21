from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('inicio', views.inicio_user, name='inicio_user'),
    path('register', views.register, name='registrarse'),
    path('login', views.login_user, name='iniciarsesion'),
    path('logout', views.logout_user, name='cerrarsesion'),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', success_url='password-reset/done/'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('mensaje_user', views.mensaje_user, name='mensaje_user'),
    path('perfil', views.perfil_user, name='perfil_user'),
    path('perfil/personal-info', views.personal_info, name='personal-info'),
    path('perfil/facturacion/crear', views.facturacion_crear , name='facturacion_crear'),
    path('perfil/facturacion/editar/<int:pk>', views.facturacion_editar , name='facturacion_editar'),
    path('perfil/facturacion/borrar/<int:pk>', views.facturacion_borrar , name='facturacion_borrar'),
    
]