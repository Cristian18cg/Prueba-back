from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import AuthenticationFailed



class IsSuperUser(permissions.BasePermission):
    """
    Permiso personalizado para restringir el acceso solo a superusuarios.

    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Verificar si los datos son válidos
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        # Generar tokens JWT para el usuario registrado
        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        #La respuesta contiene los datos basicos del usuario
        
        return Response(response_data, status=status.HTTP_201_CREATED)
   
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"detail": "An error occurred during logout."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # Verifica si el usuario está autenticado
            if not request.user.is_authenticated:
                raise AuthenticationFailed("El usuario no está autenticado.")

            # Obtén la información del usuario
            user = request.user
            return Response({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_superuser': user.is_superuser,
            }, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            # Manejo explícito para errores de autenticación
            return Response({
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            # Manejo generico de errores inesperados
            return Response({
                'error': 'Ha ocurrido un error inesperado.',
                'details': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)