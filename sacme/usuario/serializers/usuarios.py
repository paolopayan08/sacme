from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password

from django.db import transaction
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from usuario.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'second_last_name',

        ]
        read_only_fields = ('id',)


class UsuarioLoginSerializer(TokenObtainPairSerializer):
        
    default_error_messages = {
        'default': 'La información no coincide.',   
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.EmailField()

    def validate_email(self, email):
        
        existe = Usuario.objects.filter(email=email, eliminado=False).exists()
        if not existe : 
            raise serializers.ValidationError(self.default_error_messages['default'])
        return email

    def validate(self, data):
        backend = AllowAllUsersModelBackend()
        usuario = backend.authenticate(
            request=self.context,
            username=data['email'],
            password=data['password']
        )
    
        return super().validate(data)

    @classmethod
    def get_token(cls, user):
        response = super(UsuarioLoginSerializer, cls).get_token(user)

        # Custom claims
        response['sub'] = user.pk
        response['name'] = user.get_full_name()
        response['email'] = user.email

        return response


class UsuarioRegistroSerializer(serializers.Serializer):
    """
    serializer para realizar el registro del usuario mediante los
    datos obligatorios
    """
    id = serializers.ReadOnlyField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, data):
        """
        valida que el email ingresado no exista 
        """
        usuario = Usuario.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            email=data,
        )
        if len(usuario) != 0:
            raise serializers.ValidationError(
                'Este email ya esta asignado a una cuenta')
        return data

    def validate_username(self, data):
        """
        valida que el username ingresado no exista 
        """
        usuario = Usuario.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            username=data,
        )
        if len(usuario) != 0:
            raise serializers.ValidationError(
                'Este username ya esta asignado a una cuenta')
        return data

    def validate_numero_de_celular(self, data):
        """
            valida que no se repita el numero de celular
        """
        numero = Usuario.objects.filter(
            ~Q(id=self.instance.id if self.instance is not None else None),
            numero_de_celular=data,
        )
        if len(numero) != 0:
            raise serializers.ValidationError(
                'Este numero de celular ya esta asignado a una cuenta')
        return data

    def validate_password(self, value):
        """
        Convierte la contraseña en un hash value
        """
        password_validation.validate_password(value)
        return make_password(value)

        # se crean los datos en  usuario

    def create(self, validate_data):
        with transaction.atomic():
            instance = Usuario()
            instance.email = validate_data.get('email')
            instance.username = validate_data.get('username')
            instance.first_name = validate_data.get('first_name')
            instance.last_name = validate_data.get('last_name')
            instance.password = validate_data.get('password')
            instance.save()
            return instance