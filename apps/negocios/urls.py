from django.urls import path,include
from .views import NegociosViewSet, AgenteWellnessBot
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'negocios',NegociosViewSet,basename='negocios')
router.register(f'agente_3',AgenteWellnessBot,basename='agente-api')

urlpatterns = [
    path('',include(router.urls))
]