from django.contrib import admin
from .models import Vuelo, usuarios, puestos
# Register your models here.
admin.site.register(Vuelo)
admin.site.register(puestos)
admin.site.register(usuarios)
