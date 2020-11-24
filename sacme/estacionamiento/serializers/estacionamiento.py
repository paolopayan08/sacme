from django.db.models import Q

from rest_framework import serializers

from estacionamiento.models import Estacionamientos
from estacionamiento.models import Roles
from estacionamiento.models import LugaresOcupados


class EstacionamientosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estacionamientos
        fields = [
            'id',
            'nombre',
            'roles',
        ]
        read_only_fields = ('id',)

    def validate_nombre(self, valor):
        """Normalización para nombre

        Formatos:
        - Capitalización
        """
        return valor.capitalize()


class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Roles
        fields = [
            'id',
            'nombre',
            'descripcion',
        ]
        read_only_fields = ('id',)

    def validate_nombre(self, valor):
        """Normalización para nombre

        Formatos:
        - Capitalización
        """
        return valor.capitalize()


    def validate_descripcion(self, valor):
        """Normalización para descripcion

        Formatos:
        - Capitalización
        """
        return valor.capitalize()


class LugaresOcupadosSerializer(serializers.ModelSerializer):

    class Meta:
        model = LugaresOcupados
        fields = [
            'id',
            'fecha_inicio',
            'fecha_fin',
            'estacionamiento',
        ]
        read_only_fields = ('id',)