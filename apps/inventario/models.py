from django.db import models
from apps.negocios.models import Negocios

# Create your models here.

class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activo = models.BooleanField()
    fecha_creacion = models.DateTimeField(auto_now_add=True) 

class Productos(models.Model):
    negocio_id = models.ForeignKey(
        Negocios,
        on_delete=models.CASCADE,
        related_name='negocio'
    )
    codigo = models.CharField(max_length=100,unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria_id = models.ForeignKey(
        Categorias,
        on_delete=models.CASCADE,
        related_name='categoria'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Alertas(models.Model):
    producto_id = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        related_name='producto'
    )
    TIPO_ALERTA = [
        ('normal','Todo bien'),
        ('stock_bajo','Stock bajo'),
        ('vencimiento','Vencimiento proximo')
    ]
    tipo = models.CharField(max_length=100,choices=TIPO_ALERTA,default='normal')
    mensaje = models.TextField()
    activa = models.BooleanField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)