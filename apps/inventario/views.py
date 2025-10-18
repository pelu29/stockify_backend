from rest_framework import viewsets
from .models import Productos
from .serializers import ProductosSerializer

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer
