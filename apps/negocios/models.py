from django.db import models

# Create your models here.

class Negocios(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.IntegerField(null=True)
    direccion = models.CharField(max_length=100)
    propietario_id = models.ForeignKey(
        'usuarios.Clientes',
        on_delete=models.CASCADE,
        related_name='propietario'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField()
    fecha_limite_pago = models.DateField(null=True, blank=True)
    fecha_ultimo_pago = models.DateTimeField(null=True, blank=True)
    ESTADO = [
        ('pendiente','Pendiente'),
        ('parcial','Parcialmente pagado'),
        ('completo','Pagado completo'),
        ('vencido','Vencido')
    ]
    estado_pago = models.CharField(max_length=20,choices=ESTADO,default='pendiente')
    monto = models.IntegerField()
    mensaje_bloqueo = models.TextField()