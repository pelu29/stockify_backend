from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_creacion', 'total', 'estado')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('cliente__username', 'id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'producto', 'cantidad', 'subtotal')
    list_filter = ('order__estado',)
    search_fields = ('producto__nombre', 'order__id')
