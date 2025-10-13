from django.urls import path
from .views import test_view

urlpatterns = [
    path('api/test/', test_view, name='test-view'),
]
