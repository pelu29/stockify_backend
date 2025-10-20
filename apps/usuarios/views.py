from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Clientes
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
