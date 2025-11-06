from rest_framework import serializers
from .models import Producto

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    # Validaciones personalizadas
    def validate_nombre(self, value):
        if not value:
            raise serializers.ValidationError("El nombre del producto es obligatorio.")
        return value

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    # Soporte para actualizaciones parciales
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
