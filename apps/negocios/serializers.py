from rest_framework import serializers
from .models import Negocios

class NegociosSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Negocios

class InstructionSerializer(serializers.Serializer):
    instruction = serializers.CharField(max_length=500)

class ResponseSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=1000)