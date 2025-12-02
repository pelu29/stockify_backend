from django.urls import path,include
from .views import NegociosViewSet
from rest_framework.routers import DefaultRouter
from .views import FocusBuddyView

router = DefaultRouter()
router.register(f'negocios',NegociosViewSet,basename='negocios')

urlpatterns = [
    path('',include(router.urls)),
    path("focusbuddy/", FocusBuddyView.as_view(), name="focusbuddy"),
]