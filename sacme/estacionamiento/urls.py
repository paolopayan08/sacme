from django.urls import include
from django.urls import path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('estacionamientos', views.EstacionamientosView)
router.register('roles', views.RolesView)
router.register('lugares-ocupados', views.LugaresOcupadosView)

app_name = 'estacionamiento'

urlpatterns = [
    path('', include(router.urls)),
]
