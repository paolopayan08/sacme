from rest_framework import viewsets


from estacionamiento.models import Estacionamientos
from estacionamiento.models import Roles
from estacionamiento.models import LugaresOcupados

from estacionamiento.serializers import EstacionamientosSerializer
from estacionamiento.serializers import RolesSerializer
from estacionamiento.serializers import LugaresOcupadosSerializer


class EstacionamientosView(viewsets.ModelViewSet):
    queryset = Estacionamientos.objects.all()
    serializer_class = EstacionamientosSerializer

class RolesView(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer

class LugaresOcupadosView(viewsets.ModelViewSet):
    queryset = LugaresOcupados.objects.all()
    serializer_class = LugaresOcupadosSerializer