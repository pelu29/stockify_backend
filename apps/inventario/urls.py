from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductosViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'productos', ProductosViewSet, basename='productos')

# ✅ Aquí separamos las rutas manuales
manual_urls = [
    path('reports/stock/', ProductosViewSet.reporte_stock, name='reporte_stock'), #Cambiado reporte_stock por ProductosViewSet.reporte_stock
]

# ✅ Unimos ambas listas de rutas
urlpatterns = [
    path('', include(router.urls)),
]
