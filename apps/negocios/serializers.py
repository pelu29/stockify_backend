from rest_framework import serializers
from .models import Negocios

class NegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocios
        fields = '__all__'
