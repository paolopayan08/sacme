from django.db import models


class Roles(models.Model):

    descripcion = models.CharField(max_length=50, null=False, blank=False,
                                   help_text='Descripción del rol')

    nombre = models.CharField(max_length=50, null=True, blank=True,
                              help_text='Nombre del rol')

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.nombre)


class Estacionamientos(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True,
                              help_text='Nombre del estacionamiento')

    roles = models.ForeignKey('Roles', on_delete=models.DO_NOTHING,
                              help_text='Fk para conocer el rol asociado al estacionamiento')

    class Meta:
        verbose_name = 'Estacionamiento'
        verbose_name_plural = 'Estacionamientos'

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.nombre)


class LugaresOcupados(models.Model):

    fecha_inicio = models.DateField(null=False, blank=False, help_text='Fecha de la creacion del '
                                                                        'registro')
    fecha_fin = models.DateField(null=False, blank=False, help_text='Fecha de modificacion '
                                                                             'del registro')

    estacionamiento = models.ForeignKey('Estacionamientos', on_delete=models.DO_NOTHING,
                              help_text='Fk para conocer el estacionamiento ocupado')

    class Meta:
        verbose_name = 'Lugar Ocupado'
        verbose_name_plural = 'Lugares Ocupados'

    def __str__(self):
        return "{0}".format(self.pk)