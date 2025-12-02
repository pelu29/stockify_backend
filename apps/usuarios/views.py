from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Clientes
from .serializers import ClienteSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        # Serializar y validar datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cliente = serializer.save()

        # Generar un JWT real para el usuario recién creado
        token = str(AccessToken.for_user(cliente))

        # Crear respuesta JSON
        response = JsonResponse({
            "message": "Cliente creado y login correcto",
            "cliente": serializer.data
        }, status=status.HTTP_201_CREATED)

        # Configurar cookie segura con HttpOnly
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,              # evita acceso desde JS
            secure=not settings.DEBUG,  # True en producción con HTTPS
            samesite="Strict",          # protege contra CSRF
            max_age=3600,               # 1 hora
        )

        return response
