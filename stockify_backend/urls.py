from django.contrib import admin
from django.urls import path
from productos.views import ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', ProductListView.as_view()),
]