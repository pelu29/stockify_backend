from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Productos, Categorias, Negocios

class CategoriaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        validators=[UniqueValidator(queryset=Categorias.objects.all())]
    )
    descripcion = serializers.CharField(
        required = False
    )
    class Meta:
        model = Categorias
        fields = '__all__'
        

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'
        extra_kwargs = {
            'precio': {'min_value': 0},
            'stock': {'min_value': 0},
        }
