# productos/views.py

from rest_framework.views import APIView
from rest_framework.response import Response

from .products_data import productos_simulados

class ProductListView(APIView):
    def get(self, request):
       
        products = productos_simulados
        
      
        return Response(products)