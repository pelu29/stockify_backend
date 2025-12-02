from django.urls import path,include
from .views import NegociosViewSet, ejecutar_agente
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'negocios',NegociosViewSet,basename='negocios')

urlpatterns = [
    path('',include(router.urls)),
    path("agente/", ejecutar_agente, name="ejecutar_agente"),
]