from django.contrib import admin
from .models import Vuelo, puestos, aerolinea
from users.models import user
# Register your models here.
admin.site.register(aerolinea)
admin.site.register(Vuelo)
admin.site.register(puestos)
admin.site.register(user)
