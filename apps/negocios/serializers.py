from rest_framework import serializers
from .models import Negocios

class NegociosSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Negocios