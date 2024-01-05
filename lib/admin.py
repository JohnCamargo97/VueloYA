from django.contrib import admin
from .models import Vuelo, puestos, aerolinea, userVueloYa

# Register your models here.
admin.site.register(aerolinea)
admin.site.register(Vuelo)
admin.site.register(puestos)
admin.site.register(userVueloYa)
