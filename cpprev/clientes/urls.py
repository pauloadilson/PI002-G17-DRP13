from django.urls import path
from clientes.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
