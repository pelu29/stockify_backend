from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Clientes(AbstractUser):
    negocio = models.ForeignKey(
        'negocios.Negocios',
        on_delete=models.CASCADE,
        related_name='clientes'
    )
    telefono = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now=True)