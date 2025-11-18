from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductosViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'productos', ProductosViewSet, basename='productos')


# ✅ Unimos ambas listas de rutas
urlpatterns = [
    path('', include(router.urls)),
]
