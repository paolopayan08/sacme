from django.contrib import admin

from .models import Estacionamientos
from .models import Roles
from .models import LugaresOcupados
# Register your models here.


admin.site.register(Estacionamientos)
admin.site.register(Roles)
admin.site.register(LugaresOcupados)