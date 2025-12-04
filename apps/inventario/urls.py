from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductosViewSet
router = DefaultRouter()
router.register(r'categories', CategoriaViewSet, basename='categories')
router.register(r'products', ProductosViewSet, basename='products')

# ✅ Aquí separamos las rutas manuales
manual_urls = [
    path('reports/stock/',ProductosViewSet.reporte_stock, name='reporte_stock'),
]

# ✅ Unimos ambas listas de rutas
urlpatterns = manual_urls + [
    path('', include(router.urls)),
]
