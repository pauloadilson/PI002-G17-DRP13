from django.test import TestCase, Client
from django.urls import reverse
from clientes.views import IndexView
import json

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(response.context_data["page_title"], "Página inicial")
        self.assertContains(response, "Página inicial")