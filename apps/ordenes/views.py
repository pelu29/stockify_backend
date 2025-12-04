from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer
from apps.inventario.models import Productos  # Modelo correcto


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las órdenes y sus items.
    Permite crear, listar, actualizar y eliminar órdenes de forma segura.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def get_queryset(self):
        """Filtra las órdenes para que el usuario solo vea las suyas."""
        return Order.objects.filter(cliente=self.request.user)

    # ---------------- VALIDACIÓN AUXILIAR ---------------- #
    def validar_items(self, items):
        """
        Valida existencia y stock de los productos en los items de la orden.
        - Verifica que los productos existan.
        - Verifica que el stock sea suficiente.
        """
        if not items:
            raise serializers.ValidationError("Debe incluir al menos un producto en la orden.")

        # Obtener IDs de productos
        producto_ids = [
            item['producto'].id if hasattr(item['producto'], 'id') else item['producto']
            for item in items
        ]

        # Consultar productos en la base de datos
        productos = Productos.objects.filter(pk__in=producto_ids)
        productos_dict = {p.pk: p for p in productos}

        # Validar existencia y stock
        for item in items:
            producto_id = item['producto'].id if hasattr(item['producto'], 'id') else item['producto']
            producto = productos_dict.get(producto_id)

            if not producto:
                raise serializers.ValidationError(f"Producto con id {producto_id} no existe.")
            if producto.stock < item['cantidad']:
                raise serializers.ValidationError(f"Stock insuficiente para {producto.nombre}.")

    # ---------------- CREAR ORDEN ---------------- #
    def create(self, request, *args, **kwargs):
        # Asegurar que el cliente sea el usuario autenticado
        request.data['cliente'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Validar los productos y stock antes de guardar
            self.validar_items(request.data.get('items', []))

            # Guardar la orden y devolver respuesta
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------- ACTUALIZAR ORDEN ---------------- #
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            # Validar cliente (no puede cambiarlo)
            if 'cliente' in serializer.validated_data and serializer.validated_data['cliente'] != request.user:
                return Response(
                    {'error': 'No puedes cambiar el cliente de la orden.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validar productos si se actualizan los items
            if 'items' in serializer.validated_data:
                self.validar_items(serializer.validated_data['items'])

            # Guardar cambios y devolver respuesta
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)