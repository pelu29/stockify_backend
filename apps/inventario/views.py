# productos/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Categorias
from .serializers import CategoriaSerializer

    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializer
