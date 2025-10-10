from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'correo', 'rol', 'activo', 'fecha_creacion')
    search_fields = ('nombre_completo', 'correo')
    list_filter = ('rol', 'activo')

