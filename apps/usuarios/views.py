from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Clientes
from .serializers import ClienteSerializer
import jwt
import datetime
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):

        # --- Aquí generas el JWT real ---
        payload = {
            "id": 123,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, "SECRET_KEY", algorithm="HS256")

        # --- Respuesta ---
        response = JsonResponse({"message": "Login correcto"})

        # --- Cookie segura ---
    def create(request,*args, **kwargs):
        token = "mi_super_jwt"
        
        response = JsonResponse({"message": "Login correcto"})

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
          
            secure=True,      # en producción debe estar activado
            samesite="Strict",  
            max_age=3600,     # 1 hora
        )

        return response   # <<< IMPORTANTE
  
            secure=True,
            samesite="Strict",
            max_age=3600,
        )
        return response
