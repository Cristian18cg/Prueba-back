from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.db import transaction, IntegrityError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
import re
import logging
logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Este correo ya está en uso."
            )
        ],
        error_messages={
            'required': 'El correo es obligatorio.',
            'invalid': 'Ingrese un correo electrónico válido.'
        }
    )
    first_name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El nombre es obligatorio.'
        }
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El apellido es obligatorio.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        error_messages={
            'required': 'La contraseña es obligatoria.'
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Debe confirmar la contraseña.'
        }
    )
  
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate_password(self, value):
        """Valida que la contraseña cumpla con los requisitos específicos."""
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("La contraseña debe incluir al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe incluir al menos un carácter especial.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        user = None
        try:
            with transaction.atomic():
                # Crear el usuario
                user = User.objects.create(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
                )
                user.set_password(validated_data['password'])
                user.save()

        except IntegrityError as e:
            if user:
                user.delete()
            raise serializers.ValidationError({"error": "Hubo un problema al registrar al usuario. Por favor, intenta de nuevo."})

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar datos adicionales al token
        token['email'] = user.email
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            # Solo devolver el token en el login
        except Exception as e:
            logger.error("Error en la autenticación: %s", e)
            raise AuthenticationFailed("Error en la autenticación. Por favor revisa tus credenciales.")
        
        return data
