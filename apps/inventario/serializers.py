from rest_framework import serializers
from .models import Productos, Categorias, Negocios

class ProductosSerializer(serializers.ModelSerializer):
    negocio_id = serializers.PrimaryKeyRelatedField(queryset=Negocios.objects.all())
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categorias.objects.all())

    class Meta:
        model = Productos
        fields = '__all__'
        extra_kwargs = {
            'nombre': {'required': True},
            'precio': {'min_value': 0},
            'stock': {'min_value': 0},
        }
