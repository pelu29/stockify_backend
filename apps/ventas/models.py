from django.db import models
from apps.inventario.models import Productos
from apps.negocios.models import Negocios
from apps.usuarios.models import Clientes

class Venta(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_realizadas')
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE, related_name='ventas_negocio')

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.cantidad} de {self.producto.nombre} por {self.total}"
