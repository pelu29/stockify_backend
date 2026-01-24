from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductosViewSet, AlertasViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'productos', ProductosViewSet, basename='productos')
router.register(r'alertas', AlertasViewSet, basename='alertas')

# ✅ Unimos ambas listas de rutas
urlpatterns = [
    path('', include(router.urls)),
]
