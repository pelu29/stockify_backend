from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.usuarios.models import Clientes

class ClienteTests(APITestCase):
    def setUp(self):
        self.cliente1 = Clientes.objects.create_user(
            username='testuser1', email='test1@example.com', password='pass1', telefono=111111
        )
        self.cliente2 = Clientes.objects.create_user(
            username='testuser2', email='test2@example.com', password='pass2', telefono=222222
        )
        self.cliente3 = Clientes.objects.create_user(
            username='testuser3', email='test3@example.com', password='pass3', telefono=333333
        )
        self.client_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword', 'telefono': 123456789}
        self.cliente = Clientes.objects.create_user(**self.client_data)

    def test_get_cliente_list(self):
        url = reverse('clientes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(len(response.data['results']), 4)

    def test_get_cliente_detail(self):
        url = reverse('clientes-detail', args=[self.cliente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_create_cliente(self):
        url = reverse('clientes-list')
        new_client_data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'newpassword', 'telefono': 987654321}
        response = self.client.post(url, new_client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Clientes.objects.count(), 5)
        self.assertEqual(Clientes.objects.get(id=response.data['id']).username, 'newuser')

    def test_partial_update_cliente(self):
        url = reverse('clientes-detail', args=[self.cliente.id])
        data = {'telefono': 111222333}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.telefono, 111222333)

    def test_delete_cliente(self):
        url = reverse('clientes-detail', args=[self.cliente.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Clientes.objects.filter(id=self.cliente.id).exists())
