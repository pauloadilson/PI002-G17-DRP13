from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func.view_class.__name__, 'IndexView')

    def test_clientes_url_resolves(self):
        url = reverse("clientes")
        self.assertEqual(resolve(url).func.view_class.__name__, "ClientesListView")

    def test_novo_cliente_url_resolves(self):
        url = reverse("novo_cliente")
        self.assertEqual(resolve(url).func.view_class.__name__, "ClienteCreateView")