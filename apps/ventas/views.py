from rest_framework import viewsets
from .models import Venta, Ordenes
from .serializers import VentaSerializer, OrdenSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class OrdenesViewSet(viewsets.ModelViewSet):
    queryset = Ordenes.objects.all()
    serializer_class = OrdenSerializer
