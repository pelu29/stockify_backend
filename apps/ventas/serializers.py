from rest_framework import serializers
from .models import Venta, Ordenes

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'total', 'fecha_venta', 'usuario', 'negocio']
        read_only_fields = ['total', 'fecha_venta']

    def create(self, validated_data):
        # El cálculo del total se realiza en el método save del modelo Venta
        return Venta.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.producto = validated_data.get('producto', instance.producto)
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.precio_unitario = validated_data.get('precio_unitario', instance.precio_unitario)
        instance.usuario = validated_data.get('usuario', instance.usuario)
        instance.negocio = validated_data.get('negocio', instance.negocio)
        # El total se recalcula automáticamente en el método save del modelo
        instance.save()
        return instance
    
class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordenes
        fields = '__all__'