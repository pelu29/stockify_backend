from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Clientes
from .serializers import ClienteSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer

    def create(request,*args, **kwargs):
        token = "mi_super_jwt"
        
        response = JsonResponse({"message": "Login correcto"})

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=3600,
        )
        return response
