from rest_framework import viewsets
from .models import Productos,Categorias, Alertas
from .serializers import ProductosSerializer, CategoriaSerializer, AlertaSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.inventario.pagination import CustomPagination
    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.order_by('pk')
    serializer_class = ProductosSerializer
    pagination_class = CustomPagination

class AlertasViewSet(viewsets.ModelViewSet):
    queryset = Alertas.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [IsAuthenticated]