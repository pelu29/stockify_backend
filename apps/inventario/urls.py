from apps.inventario.views import CategoriaViewSet
from apps.inventario.views import ProductosViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include


router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductosViewSet)

urlpatterns = [
    path('',include(router.urls))
]