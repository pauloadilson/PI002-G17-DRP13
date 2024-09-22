from django.test import TestCase, Client
from django.urls import reverse
import json

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.clientes_url = reverse("clientes")
        self.novo_cliente_url = reverse("novo_cliente")

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(response.context_data["page_title"], "Página inicial")
        self.assertContains(response, "Página inicial")
    
    def test_ClientesListView_GET(self):
        response = self.client.get(self.clientes_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clientes.html")
        self.assertEqual(response.context_data["page_title"], "Clientes")

    def test_ClienteCreateView_GET(self):
        response = self.client.get(self.novo_cliente_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")
        self.assertEqual(response.context_data["page_title"], "Novo Cliente")
        self.assertEqual(response.context_data["form_title"], "Novo Cliente")
    
    def test_ClienteCreateView_POST(self):
        response = self.client.post(self.novo_cliente_url, {
            "cpf": "12345678901",
            "nome": "Fulano de Tal",
            "data_nascimento": "1981-01-21",
            "telefone_whatsapp": "18991234567",
            "email": "paulo@paulo.com",
        })

        # First, check for the 302 redirect
        self.assertEqual(response.status_code, 302)

        # Now, follow the redirect
        follow_response = self.client.get(response.url)

        # Check that the redirect leads to the correct page
        self.assertEqual(follow_response.status_code, 200)

        # Now check the response contains the expected data (if applicable on the redirected page)
        self.assertTemplateUsed(follow_response, "clientes.html")


        
