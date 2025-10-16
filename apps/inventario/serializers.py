from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Productos
from .models import Categorias

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['id', 'name', 'category', 'price', 'description', 'created_at']

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
