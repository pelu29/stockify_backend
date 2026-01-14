from rest_framework import serializers
from .models import Venta
from ..inventario.models import Productos
from ..negocios.models import Negocios
from ..usuarios.models import Clientes

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'total', 'fecha_venta', 'usuario', 'negocio']
        read_only_fields = ['total', 'fecha_venta']

    # Validaciones de campos individuales
    def validate_cantidad(self, value):
        """Validar que cantidad sea mayor a 0"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value

    def validate_precio_unitario(self, value):
        """Validar que precio_unitario sea mayor a 0"""
        if value <= 0:
            raise serializers.ValidationError("El precio unitario debe ser mayor a 0")
        return value

    # Validación a nivel del objeto completo
    def validate(self, data):
        """Validaciones que dependen de múltiples campos"""
        producto = data.get('producto')
        cantidad = data.get('cantidad')
        precio_unitario = data.get('precio_unitario')
        negocio = data.get('negocio')
        usuario = data.get('usuario')

        # 1. Validar que el producto existe y está activo
        if producto:
            if not isinstance(producto, Productos):
                raise serializers.ValidationError("El producto debe ser válido")
            # Validar que el producto pertenece al negocio
            if producto.negocio_id != negocio:
                raise serializers.ValidationError("El producto no pertenece al negocio seleccionado")

        # 2. Validar stock disponible
        if producto and cantidad:
            if producto.stock < cantidad:
                raise serializers.ValidationError(
                    f"Stock insuficiente. Stock disponible: {producto.stock}, cantidad solicitada: {cantidad}"
                )

        # 3. Validar que el negocio es válido y está activo
        if negocio:
            if not isinstance(negocio, Negocios):
                raise serializers.ValidationError("El negocio debe ser válido")
            if not negocio.activo:
                raise serializers.ValidationError("El negocio está inactivo")

        # 4. Validar que el usuario existe (si se proporciona)
        if usuario:
            if not isinstance(usuario, Clientes):
                raise serializers.ValidationError("El usuario debe ser válido")

        # 5. Validar cálculo del total
        if cantidad and precio_unitario:
            total_calculado = cantidad * precio_unitario
            if total_calculado < 0:
                raise serializers.ValidationError("El total no puede ser negativo")

        return data

    def create(self, validated_data):
        """Crear venta y descontar del stock"""
        venta = Venta.objects.create(**validated_data)
        # Descontar stock del producto
        producto = venta.producto
        producto.stock -= venta.cantidad
        producto.save()
        return venta

    def update(self, instance, validated_data):
        """Actualizar venta y ajustar stock"""
        # Restaurar stock anterior si la cantidad cambió
        cantidad_anterior = instance.cantidad
        cantidad_nueva = validated_data.get('cantidad', instance.cantidad)
        
        if cantidad_anterior != cantidad_nueva:
            producto = instance.producto
            # Restaurar stock viejo
            producto.stock += cantidad_anterior
            # Descontar stock nuevo
            producto.stock -= cantidad_nueva
            producto.save()

        instance.producto = validated_data.get('producto', instance.producto)
        instance.cantidad = cantidad_nueva
        instance.precio_unitario = validated_data.get('precio_unitario', instance.precio_unitario)
        instance.usuario = validated_data.get('usuario', instance.usuario)
        instance.negocio = validated_data.get('negocio', instance.negocio)
        instance.save()
        return instance
