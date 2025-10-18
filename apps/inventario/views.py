from rest_framework import viewsets
from .models import Productos
from .serializers import ProductosSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Categorias
from .serializers import CategoriaSerializer

    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializer

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer