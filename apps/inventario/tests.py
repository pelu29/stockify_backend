from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.inventario.models import Categorias, Productos, Alertas
from apps.negocios.models import Negocios
from apps.usuarios.models import Clientes

cliente_data ={"username":"User","telefono":000000000}
class CategoriaTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cliente_data = cliente_data
        self.cliente = Clientes.objects.create_user(**self.cliente_data)
        self.client.force_authenticate(user=self.cliente)
        self.categoria = Categorias.objects.create(
            nombre="Bebidas",
            descripcion="Productos líquidos",
            activo=True
        )
        self.url = reverse("categorias-list")

    def test_get_categoria(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_categoria(self):
        data = {"nombre": "Snacks", "descripcion": "Comida rápida", "activo": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_categoria(self):
        url_detail = reverse("categorias-detail", args=[self.categoria.id])
        response = self.client.patch(url_detail, {"descripcion": "Nueva descripción"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["descripcion"], "Nueva descripción")

    def test_delete_categoria(self): # No se elimina la categoria, se desactiva
        url_detail = reverse("categorias-detail", args=[self.categoria.id])
        response = self.client.patch(url_detail, {"activo": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categoria = Categorias.objects.get(id=self.categoria.id)
        self.assertFalse(categoria.activo)



class ProductoTests(APITestCase):
    def setUp(self):
        self.cliente_data = cliente_data
        self.cliente = Clientes.objects.create(**self.cliente_data)

        self.negocio_data = {"id":1,"nombre":"negocioPrueba","activo":True,"monto":15000,"propietario_id":self.cliente}
        self.negocio = Negocios.objects.create(**self.negocio_data)
        
        self.categoria = Categorias.objects.create(nombre="Lácteos", descripcion="Derivados", activo=True)
        self.producto = Productos.objects.create(
            negocio_id=self.negocio,
            codigo="P001",
            nombre="Leche",
            descripcion="Leche fresca",
            categoria_id=self.categoria,
            precio=5.50,
            stock=10,
            stock_minimo=2
        )
        self.url = reverse("productos-list")

    def test_get_producto(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_producto(self):
        data = {
            "negocio_id": self.negocio.id,
            "codigo": "P002",
            "nombre": "Yogurt",
            "descripcion": "Yogurt natural",
            "categoria_id": self.categoria.id,
            "precio": 3.20,
            "stock": 15,
            "stock_minimo": 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_producto(self):
        url_detail = reverse("productos-detail", args=[self.producto.id])
        response = self.client.patch(url_detail, {"precio": 6.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["precio"]), 6.00)

    def test_delete_producto(self):
        url_detail = reverse("productos-detail", args=[self.producto.id])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Productos.objects.filter(id=self.producto.id).exists())


class AlertaTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cliente_data = cliente_data
        self.cliente = Clientes.objects.create_user(**self.cliente_data)
        self.client.force_authenticate(user=self.cliente)

        self.categoria = Categorias.objects.create(
            nombre="Panadería", descripcion="Harinas", activo=True
        )
        self.producto = Productos.objects.create(
            codigo="P003",
            nombre="Pan",
            descripcion="Pan integral",
            categoria_id=self.categoria,
            precio=1.50,
            stock=50,
            stock_minimo=10
        )
        self.alerta = Alertas.objects.create(
            producto_id=self.producto,
            tipo="stock_bajo",
            mensaje="El stock está bajo",
            activa=True
        )
        self.url = reverse("alertas-list")

    def test_get_alerta(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_alerta(self):
        data = {
            "producto_id": self.producto.pk,
            "tipo": "vencimiento",
            "mensaje": "Producto por vencer",
            "activa": True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_alerta(self):
        url_detail = reverse("alertas-detail", args=[self.alerta.id])
        response = self.client.patch(url_detail, {"activa": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["activa"], False)

    def test_delete_alerta(self):  # No se elimina la alerta, en su lugar se desactiva
        url_detail = reverse("alertas-detail", args=[self.alerta.id])
        response = self.client.patch(url_detail, {"activa": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alerta = Alertas.objects.get(id=self.alerta.id)
        self.assertFalse(alerta.activa)
