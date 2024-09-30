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

    def test_cliente_detail_url_resolves(self):
        url = reverse("cliente", args=[1])
        self.assertEqual(resolve(url).func.view_class.__name__, "ClienteDetailView")

    def test_novo_requerimento_url_resolves(self):
        url = reverse("novo_requerimento")
        self.assertEqual(resolve(url).func.view_class.__name__, "RequerimentoCreateView")

    def test_requerimento_detail_url_resolves(self):
        url = reverse("requerimento", args=[1])
        self.assertEqual(resolve(url).func.view_class.__name__, "RequerimentoDetailView")

    def test_nova_exigencia_url_resolves(self):
        url = reverse("nova_exigencia")
        self.assertEqual(resolve(url).func.view_class.__name__, "ExigenciaCreateView")
        