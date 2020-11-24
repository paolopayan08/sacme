from django.utils import timezone
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet


from usuario.models import Usuario
from usuario.serializers import UsuarioSerializer
from usuario.serializers import UsuarioLoginSerializer
from usuario.serializers import UsuarioRegistroSerializer


class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class LoginView(TokenObtainPairView):
    """
    clase login para iniciar sesion en base a serializer 
    CiudadanoLoginCiudadano
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UsuarioLoginSerializer

    """
    Se mandan parametros extras para el login, aparte del token
    se manda el last_login
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        content = serializer.validated_data
        usuario = serializer.user
        content['last_login'] = usuario.last_login
        usuario.last_login = timezone.now()
        usuario.save()
        return Response(content, status=status.HTTP_200_OK)


class UsuarioRegistroView(APIView):
    """
        Vista para crear modelo obteniendo request de UsuarioRegistroSerializer
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UsuarioRegistroSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        usuario = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UsuarioIdView(GenericViewSet):
    """
        Vista para referenciar el modelo usuario donde se
        obtiene el usuario logueado
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UsuarioSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = request.method.lower() == 'patch'
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
