from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Clientes

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_email(self, value):
        if Clientes.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def validate_telefono(self, value):
        value_str = str(value)
        digitos= ''.join(c for c in value_str if c.isdigit())

        if len(digitos) != 9:
            raise serializers.ValidationError("El telefono solo puede tener 9 digitos")
        
        if Clientes.objects.filter(telefono=int(value_str)).exists():
            raise serializers.ValidationError("Este numero ya ha sido registrado")
        
        digitos = int(digitos)
        return digitos



    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


