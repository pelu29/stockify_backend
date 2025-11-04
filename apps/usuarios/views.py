from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Clientes
from .serializers import ClienteSerializer
from rest_framework.permissions import IsAuthenticated

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer