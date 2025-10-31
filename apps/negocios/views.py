from rest_framework import viewsets
from .models import Negocios
from .serializers import NegociosSerializer

class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer
