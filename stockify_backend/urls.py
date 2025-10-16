from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.inventario.views import ProductListView
from apps.inventario.views import CategoriaViewSet




router = DefaultRouter()
router.register(r'api/categorias', CategoriaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', ProductListView.as_view()),
    path('', include(router.urls)),
]
