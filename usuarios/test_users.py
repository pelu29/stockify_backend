# test_users.py
class TestUser:
    def __init__(self, nombre_completo, correo, rol, activo):
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.rol = rol
        self.activo = activo

# Crear usuarios de prueba
usuarios_prueba = [
    TestUser("Administrador Prueba", "admin@example.com", "administrador", True),
    TestUser("Cajero Prueba", "cajero@example.com", "cajero", True),
    TestUser("Contador Prueba", "contador@example.com", "contador", True)
]
