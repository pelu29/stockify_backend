from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductSerializer
from bitacora.models import Actividad  # 👈 Importa la bitácora

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        producto = serializer.save()
        # Registrar acción en la bitácora
        Actividad.objects.create(
            accion="Creación de producto",
            usuario="Sistema",  # puedes reemplazar por el usuario real si luego agregas auth
            detalle=f"Se creó el producto '{producto.nombre}' con precio {producto.precio} y stock {producto.stock}."
        )

    def perform_update(self, serializer):
        producto = serializer.save()
        Actividad.objects.create(
            accion="Actualización de producto",
            usuario="Sistema",
            detalle=f"Se actualizó el producto '{producto.nombre}'."
        )

    def perform_destroy(self, instance):
        nombre = instance.nombre
        instance.delete()
        Actividad.objects.create(
            accion="Eliminación de producto",
            usuario="Sistema",
            detalle=f"Se eliminó el producto '{nombre}'."
        )

    # Para permitir actualizaciones parciales (PATCH)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) or request.method == 'PATCH'
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
