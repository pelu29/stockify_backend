from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Clientes(AbstractUser):
    telefono = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now=True)

class productos(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
