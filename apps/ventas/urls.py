from rest_framework.routers import DefaultRouter
from .views import VentaViewSet,OrdenesViewSet
from django.urls import path,include

router = DefaultRouter()
router.register(r'ventas', VentaViewSet , basename='ventas')
router.register(r'ordenes', OrdenesViewSet, basename='ordenes')

urlpatterns = [
    path('',include(router.urls))
]
