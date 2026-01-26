from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.usuarios.models import Clientes
from apps.negocios.models import Negocios

class NegociosModelTest(TestCase):
    def setUp(self):
        self.propietario = Clientes.objects.create_user(
            username='testuser',
            password='testpassword',
            telefono=123456789
        )
        self.negocio = Negocios.objects.create(
            nombre='Mi Negocio de Prueba',
            ruc=12345678901,
            direccion='Av. Siempreviva 742',
            propietario_id=self.propietario,
            activo=True,
            monto=1000,
            mensaje_bloqueo='Prueba'
        )

    def test_negocio_creacion(self):
        self.assertEqual(self.negocio.nombre, 'Mi Negocio de Prueba')
        self.assertEqual(self.negocio.propietario_id.username, 'testuser')

class NegociosViewSetTest(APITestCase):
    def setUp(self):
        self.propietario = Clientes.objects.create_user(
            username='testuser',
            password='testpassword',
            telefono=123456789
        )
        self.client.login(username='testuser', password='testpassword')
        self.negocio = Negocios.objects.create(
            nombre='Mi Negocio de Prueba',
            ruc=12345678901,
            direccion='Av. Siempreviva 742',
            propietario_id=self.propietario,
            activo=True,
            monto=1000,
            mensaje_bloqueo='Prueba'
        )
        self.negocios_url = reverse('negocios-list')
        self.negocio_detail_url = reverse('negocios-detail', kwargs={'pk': self.negocio.pk})

    def test_get_negocios_list(self):
        response = self.client.get(self.negocios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_negocio(self):
        data = {
            'nombre': 'Otro Negocio',
            'ruc': 98765432109,
            'direccion': 'Calle Falsa 123',
            'propietario_id': self.propietario.pk,
            'activo': False,
            'monto': 500,
            'mensaje_bloqueo': 'Bloqueado'
        }
        response = self.client.post(self.negocios_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Negocios.objects.count(), 2)

    def test_get_negocio_detail(self):
        response = self.client.get(self.negocio_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.negocio.nombre)

    def test_update_negocio(self):
        data = {
            'nombre': 'Negocio Actualizado',
            'ruc': 12345678901,
            'direccion': 'Av. Siempreviva 742',
            'propietario_id': self.propietario.pk,
            'activo': True,
            'monto': 1500,
            'mensaje_bloqueo': 'Prueba'
        }
        response = self.client.put(self.negocio_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.negocio.refresh_from_db()
        self.assertEqual(self.negocio.monto, 1500)

    def test_delete_negocio(self):
        response = self.client.delete(self.negocio_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Negocios.objects.count(), 0)
