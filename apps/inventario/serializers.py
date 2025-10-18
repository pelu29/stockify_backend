from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Productos, Categorias, Negocios

class CategoriaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Categorias.objects.all())]
    )
    descripcion = serializers.CharField(
        required = False
    )
    class Meta:
        model = Categorias
        fields = ['nombre' , 'descripcion', 'activo','fecha_creacion']


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
