from django.test import TestCase
from clientes.models import Cliente
from django.urls import reverse

# Create your tests here.
class TestModels(TestCase):
    def setUp(self):
        self.cliente1 = Cliente.objects.create(
            cpf="12345678901",
            nome="Fulano de Tal",
            data_nascimento="1981-01-21",
            telefone_whatsapp="18991234567",
            email="pauloadilson@gmail.com"
        )  

    def test_cliente_model(self):
        self.assertEqual(self.cliente1.cpf, "12345678901")
        self.assertEqual(self.cliente1.nome, "Fulano de Tal")
        self.assertEqual(self.cliente1.data_nascimento, "1981-01-21")
        self.assertEqual(self.cliente1.telefone_whatsapp, "18991234567")
        self.assertEqual(self.cliente1.email, "pauloadilson@gmail.com")
        self.assertEqual(self.cliente1.is_deleted, False)
        self.assertEqual(str(self.cliente1), "12345678901, Fulano de Tal, 1981-01-21, 18991234567, None, pauloadilson@gmail.com")
        self.assertEqual(self.cliente1.get_class_name(), "Cliente")
        self.cliente1.delete()
        self.assertEqual(self.cliente1.is_deleted, True)

