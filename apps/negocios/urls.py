from django.urls import path,include
from .views import NegociosViewSet, ChefAIAgentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'negocios',NegociosViewSet,basename='negocios')

urlpatterns = [
    path('chefai/', ChefAIAgentView.as_view(), name='chef_ai_agent'),
    path('',include(router.urls))
]
