from django.test import SimpleTestCase
from django.urls import reverse, resolve
from clientes.views import IndexView

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func.view_class, IndexView)