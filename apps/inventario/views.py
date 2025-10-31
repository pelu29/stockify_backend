# 📦 Django REST Framework
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 📦 Django
from django.http import HttpResponse

# 📦 Modelos y Serializers
from .models import Productos, Categorias
from .serializers import ProductosSerializer, CategoriaSerializer
from apps.negocios.models import Negocios
from apps.negocios.serializers import NegociosSerializer

# 📦 Reporte CSV y PDF
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# 🧩 ViewSets
class NegociosViewSet(viewsets.ModelViewSet):
    queryset = Negocios.objects.all()
    serializer_class = NegociosSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializer

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer

from rest_framework.decorators import api_view

def reporte_stock(request):
    formato = request.GET.get('format', 'csv')  # ?format=csv o ?format=pdf

    productos = Productos.objects.select_related('categoria_id').all()

    if not productos.exists():
        return Response({"mensaje": "No hay productos registrados para generar el reporte."}, status=204)

    data = []
    for p in productos:
        data.append({
            'Código': p.codigo,
            'Nombre': p.nombre,
            'Descripción': p.descripcion,
            'Categoría': p.categoria_id.nombre if p.categoria_id else '',
            'Precio': float(p.precio),
            'Stock': p.stock,
            'Stock mínimo': p.stock_minimo,
            'Fecha creación': p.fecha_creacion.strftime('%Y-%m-%d'),
            'Fecha actualización': p.fecha_actualizacion.strftime('%Y-%m-%d'),
        })

    if formato == 'csv':
        df = pd.DataFrame(data)
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_stock.csv"'
        return response

    elif formato == 'pdf':
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Título
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Reporte de Stock")

        # Encabezados
        p.setFont("Helvetica-Bold", 10)
        y = 720
        p.drawString(50, y, "Código")
        p.drawString(130, y, "Nombre")
        p.drawString(250, y, "Categoría")
        p.drawString(350, y, "Stock")
        p.drawString(420, y, "Precio")

        # Filas
        y -= 20
        p.setFont("Helvetica", 9)
        for item in data:
            p.drawString(50, y, str(item.get('Código', '')))
            p.drawString(130, y, str(item.get('Nombre', '')))
            p.drawString(250, y, str(item.get('Categoría', '')))
            p.drawString(350, y, str(item.get('Stock', '')))
            p.drawString(420, y, f"S/{item.get('Precio', 0):.2f}")
            y -= 20
            if y < 50:
                p.showPage()
                y = 750
                p.setFont("Helvetica", 9)

        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_stock.pdf"'
        return response

    return Response({"error": "Formato no soportado. Usa ?format=csv o ?format=pdf"}, status=400)