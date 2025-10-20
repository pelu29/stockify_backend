# usuarios/urls.py
from django.urls import path
from .views import ClienteViewSet

cliente_register = ClienteViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('register/', cliente_register, name='cliente-register'),
]
