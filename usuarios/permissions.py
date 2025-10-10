from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'rol', '') == 'administrador'

class IsCajeroUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'rol', '') == 'cajero'

class IsContadorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'rol', '') == 'contador'