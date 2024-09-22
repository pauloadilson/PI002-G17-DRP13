from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from clientes.views import IndexView, ClientesListView, ClienteCreateView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("clientes/", ClientesListView.as_view(), name="clientes"),
    path("novo_cliente/", ClienteCreateView.as_view(), name="novo_cliente"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
