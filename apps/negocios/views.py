from rest_framework import viewsets
from .models import Negocios
from .serializers import NegociosSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer
    permission_classes = [IsAuthenticated]
