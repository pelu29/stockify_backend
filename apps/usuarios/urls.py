# usuarios/urls.py
from .views import ClienteViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router = DefaultRouter()
router.register(f'clientes',ClienteViewSet,basename='clientes')

urlpatterns = [
    path('',include(router.urls)),
]


