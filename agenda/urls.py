from django.urls import path
from django.urls import path, include
from agenda.views import (
    EventoCreateView,
    AgendaView,
)
from . import views

urlpatterns = [
    path("agenda/", AgendaView.as_view(), name="agenda"),
    path("evento/adicionar", EventoCreateView.as_view(), name="adicionar_evento"),
]
