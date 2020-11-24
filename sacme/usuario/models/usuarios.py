from django.contrib.auth.models import AbstractUser
from django.db import models
from .mixins import DatosDeControlMixin

class Usuario(AbstractUser, DatosDeControlMixin):
    """
	    Datos personales del Usuario

	"""
    # Datos obligatorios
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # Datos opcionales
    second_last_name = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return "{0}-{1}".format(
            self.first_name,
            self.email,
        )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (
            self.first_name,
            self.last_name,
            self.second_last_name if self.second_last_name is not None else '',
        )
        return full_name.strip()
