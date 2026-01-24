from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.usuarios.models import Clientes
from .serializers import ClienteSerializer
from rest_framework.permissions import IsAuthenticated

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all().order_by('id')

    serializer_class = ClienteSerializer