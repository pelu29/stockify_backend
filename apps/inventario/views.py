# 📦 Django REST Framework
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 📦 Django
from django.http import HttpResponse

# 📦 Modelos y Serializers
from apps.negocios.models import Negocios
from apps.negocios.serializers import NegociosSerializer

# 🧩 ViewSets
class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer


from apps.inventario.models import Productos,Categorias, Alertas
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
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer

class AlertasViewSet(viewsets.ModelViewSet):
    queryset = Alertas.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [IsAuthenticated]
