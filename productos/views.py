from rest_framework.views import APIView
from rest_framework.response import Response

class ProductListView(APIView):
    def get(self, request):
        productos = [
            {"nombre": "Café", "categoria": "Bebidas", "precio": 10.5},
            {"nombre": "Té", "categoria": "Bebidas", "precio": 8.0},
            {"nombre": "Galleta", "categoria": "Snack", "precio": 2.5},
        ]
        return Response(productos)
