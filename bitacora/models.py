from django.db import models

class Actividad(models.Model):
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.accion} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
