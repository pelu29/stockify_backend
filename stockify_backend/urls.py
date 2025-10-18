from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.inventario.views import ProductosViewSet

router = DefaultRouter()
router.register(r'products', ProductosViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
