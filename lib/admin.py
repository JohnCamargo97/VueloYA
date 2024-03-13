from typing import Any, Mapping
from django.contrib import admin
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Vuelo, puestos, aerolinea, userVueloYa, oferta, historicoReserva


class vueloFormAdmin(admin.ModelAdmin):
    readonly_fields= ('duracion1', 'duracion2',)
    fields = ('origen', 'destino', 'fechasalida', 'horasalida1', 'horasalida2', 'duracion1', 'fechavuelta', 'horavuelta1', 'horavuelta2', 'duracion2', 'id_aerolinea', 'Escalado', 'escalas', 'precio', 'Ida_vuelta')

    
    
# Register your models here.
admin.site.register(aerolinea)
admin.site.register(Vuelo)
admin.site.register(puestos)
admin.site.register(userVueloYa)
admin.site.register(oferta)
admin.site.register(historicoReserva)