from django.contrib import admin
from django.urls import path, include  # 👈 incluye 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),  # 👈 conecta las rutas de la app productos
]
