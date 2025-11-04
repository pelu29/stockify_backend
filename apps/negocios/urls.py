from django.urls import path,include
from .views import NegociosViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'negocios',NegociosViewSet,basename='negocios')

urlpatterns = [
    path('',include(router.urls))
]