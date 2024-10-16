from django.urls import path
from django.urls import path, include
from eventos.views import (
    EventoCreateView,
    EventoListView,
)
from . import views

urlpatterns = [
    path("eventos/", EventoListView.as_view(), name="eventos"),
    path("evento/adicionar", EventoCreateView.as_view(), name="adicionar_evento"),
    #path('outlook-calendar/init/', views.outlook_calendar_init, name='outlook_calendar_init'),
    #path('callback/', views.outlook_calendar_callback, name='outlook_calendar_callback'),
    #path('outlook-calendar/events/', views.list_events, name='list_events'),
]
