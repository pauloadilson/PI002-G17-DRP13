from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
)
from agenda.models import Evento
from django.urls import reverse_lazy
from django.conf import settings
from agenda.forms import EventoForm
from login.graph_helper import criar_evento_no_microsoft_graph
from django.contrib import messages


# Create your views here.
# Exibe uma lista de eventos
class AgendaView(ListView):
    model = Evento
    template_name = 'agenda.html'
    context_object_name = 'agenda'
    title = "Agenda"
    
    def get_queryset(self):
        return Evento.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(AgendaView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

# Cria um novo evento
class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'form.html'
    success_url = reverse_lazy('agenda')
    title = "Novo Evento"

    def form_valid(self, form):
        # Primeiro, salva o evento localment
        response = super().form_valid(form)
        print('entrando no metodo')

        # Depois, tenta criar o evento no Microsoft Graph
        try:
            print('tentando criar evento no Microsoft Graph')
            # Substitua "user_email" pelo e-mail do usuário que deve receber o evento
            #user_email = settings.MICROSOFT_CLIENT_EMAIL  # Exemplo usando o e-mail do usuário logado
            criar_evento_no_microsoft_graph(self.request, self.object)  # self.object é o evento salvo
            print('evento criado no Microsoft Graph??')
            messages.success(self.request, 'Evento criado e sincronizado com o calendário do Microsoft Outlook.')
        except Exception as e:
            print(f'Erro ao criar evento no Microsoft Outlook: {e}')
            messages.error(self.request, f'Erro ao criar evento no Microsoft Outlook: {e}')

        return response


    def get_context_data(self, **kwargs):
        context = super(EventoCreateView, self).get_context_data(**kwargs)
        # adicionar o título da página e o título do formulário ao contexto
        context['title'] = self.title
        return context
    


# Edita um evento existente
class EventoUpdateView(UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'form.html'
    success_url = reverse_lazy('agenda')
    title = "Editando Evento"

    def get_context_data(self, **kwargs):
        context = super(EventoUpdateView, self).get_context_data(**kwargs)
        # adicionar o título da página e o título do formulário ao contexto
        context['title'] = self.title
        return context
    