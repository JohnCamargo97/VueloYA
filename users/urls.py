from django.urls import path, include
from lib import views as lib_views
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('inicio', user_views.inicio_user, name='inicio_user'),
    path('register', user_views.register, name='registrarse'),
    path('login', user_views.login_user, name='iniciarsesion'),
    path('logout', user_views.logout_user, name='cerrarsesion'),
    path('borrar_cuenta/<int:pk>', user_views.delete_user , name='borrar_cuenta'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', post_reset_login=True, success_url='../../../perfil'), name='password_reset_confirm'),
    #path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('mensaje_user', user_views.mensaje_user, name='mensaje_user'),
    path('perfil', user_views.perfil_user, name='perfil_user'),
    path('perfil/personal-info', user_views.personal_info, name='personal-info'),
    path('perfil/facturacion/crear', user_views.facturacion_crear , name='facturacion_crear'),
    path('perfil/facturacion/editar/<int:pk>', user_views.facturacion_editar , name='facturacion_editar'),
    path('perfil/facturacion/borrar/<int:pk>', user_views.facturacion_borrar , name='facturacion_borrar'),
    
]