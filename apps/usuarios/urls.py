# usuarios/urls.py
from .views import ClienteViewSet
from django.urls import path,include

cliente_register = ClienteViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('register/', cliente_register, name='cliente-register'),
]


