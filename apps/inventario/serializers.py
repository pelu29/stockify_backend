from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Categorias

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
