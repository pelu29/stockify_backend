from rest_framework import viewsets
from .models import Productos,Categorias
from .serializers import ProductosSerializer, CategoriaSerializer
from rest_framework.response import Response
from rest_framework import viewsets

    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializer

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer