from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):  #Serializador para los items de la orden
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True) #Obtiene el nombre del producto relacionado
    precio_unitario = serializers.DecimalField(source='producto.precio', max_digits=10, decimal_places=2, read_only=True) #Obtiene el precio del producto relacionado

    class Meta:
        model = OrderItem 
        fields = ['id', 'producto', 'producto_nombre', 'precio_unitario', 'cantidad', 'subtotal'] #Campos del serializador

class OrderSerializer(serializers.ModelSerializer): #Serializador para la orden
    orderitem_set = OrderItemSerializer(many=True, read_only=True) #Serializador anidado para los items de la orden
    items = OrderItemSerializer(many=True, write_only=True) #Campo para recibir los items al crear/actualizar una orden con validación adecuada

    class Meta:
        model = Order
        fields = ['id', 'cliente', 'fecha_creacion', 'total', 'estado', 'orderitem_set', 'items'] #Campos del serializador

    def create(self, validated_data): #Crear una nueva orden con sus items
        items_data = validated_data.pop('items') # Extraer los datos de los items
        order = Order.objects.create(**validated_data) # Crear la orden
        for item_data in items_data: # Crear cada item de la orden
            OrderItem.objects.create(order=order, **item_data)
        order.save()  # Recalcular total
        return order

    def update(self, instance, validated_data): #Actualizar una orden y sus items
        items_data = validated_data.pop('items', None) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value) 
        instance.save()

        if items_data is not None: # Actualizar, crear o eliminar items según items_data
            existing_items = {item.id: item for item in instance.orderitem_set.all()} 
            sent_item_ids = [item.get('id') for item in items_data if item.get('id')]

            # Actualizar o crear items
            for item_data in items_data:
                item_id = item_data.get('id', None)
                if item_id and item_id in existing_items:
                    # Actualizar item existente
                    item = existing_items[item_id]
                    for attr, value in item_data.items():
                        if attr != 'id':
                            setattr(item, attr, value)
                    item.save()
                else:
                    # Crear nuevo item
                    OrderItem.objects.create(order=instance, **{k: v for k, v in item_data.items() if k != 'id'})

            # Eliminar items que no están en items_data
            for item_id, item in existing_items.items():
                if item_id not in sent_item_ids:
                    item.delete()
        return instance