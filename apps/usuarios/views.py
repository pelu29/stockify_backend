from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Clientes
from .serializers import ClienteSerializer
from django.http import JsonResponse
import datetime
import jwt

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        token = "mi_clave_secreta"

        # Respuesta de creación del cliente (o cualquier acción antes de retornar la respuesta)
        response = JsonResponse({"message": "Login correcto"})

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  #Esto asegura que la cookie no sea accesible mediante JavaScript
            secure=True,  #Establecer a True en producción
            samesite="Strict",  #Permite que la cookie sea enviada en solicitudes cross-site
            max_age=3600,  #La cookie expirará en 1 hora
        )

        return response
    