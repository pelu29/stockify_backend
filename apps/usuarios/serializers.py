from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Clientes

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if Clientes.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

