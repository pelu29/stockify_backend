from django.urls import path
from .views import FocusBuddyView

urlpatterns = [
    path("focusbuddy/", FocusBuddyView.as_view(), name="focusbuddy"),
]
