from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import LoginView


router = routers.DefaultRouter()
router.register('usuarios', views.UsuarioView)

app_name = 'usuario'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name="login"),
    path('refresh-token/', TokenRefreshView.as_view(), name="refresh_token"),
    path('registro/', views.UsuarioRegistroView.as_view(), name="registro-usuario"),
    path('id/', views.UsuarioIdView.as_view({ 'get': 'retrieve', 'patch': 'update', 'put': 'update' }), name="usuario"),
]
