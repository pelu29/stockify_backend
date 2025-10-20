from django.contrib import admin
from django.urls import path, include 
from apps.inventario.views import ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', ProductListView.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('apps.usuarios.urls')),
]
