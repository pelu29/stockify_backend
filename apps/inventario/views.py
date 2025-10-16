# productos/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Categorias
from .serializers import CategoriaSerializer

from .products_data import productos_simulados

class ProductListView(APIView):
    def get(self, request):
       
        products = productos_simulados
        
      
        return Response(products)
    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializer
