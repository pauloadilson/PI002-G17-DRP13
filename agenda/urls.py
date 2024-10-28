from django.urls import path
from django.urls import path, include
from agenda.views import (
    EventoCreateView,
    AgendaView,
    EventoDetailView,
)
from . import views

urlpatterns = [
    path("agenda/", AgendaView.as_view(), name="agenda"),
    path("evento/", include([
        path("<int:pk>", EventoDetailView.as_view(), name="evento"),
        path("adicionar", EventoCreateView.as_view(), name="adicionar_evento"),
    ])),
]
