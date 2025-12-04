from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/inventario/', include('apps.inventario.urls')),
    path('api/ordenes/', include('apps.ordenes.urls')),
    #path('api/', include('apps.inventario.urls')),  # ✅ NO uses 'api/inventario/'
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('api/negocios/',include('apps.negocios.urls')),
    #path('api/ventas/', include('apps.ventas.urls')),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
     path("api/", include("focusbuddy.urls")),
     path("api/negocios/", include("apps.negocios.urls")),
]
