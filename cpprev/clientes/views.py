from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from clientes.models import Cliente
from clientes.forms import ClienteModelForm
from django.urls import reverse_lazy


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    page_title = "Página inicial"

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

class ClientesListView(ListView):
    model = Cliente
    template_name = "clientes.html"
    context_object_name = "clientes"
    page_title = "Clientes"
    ordering = ["nome"]
    paginate_by = 10

    def get_queryset(self):
        clientes = super().get_queryset().filter(is_deleted=False)
        busca = self.request.GET.get("busca")
        if busca:
            clientes = clientes.filter(cpf__icontains=busca)
        return clientes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'form.html'
    form_class = ClienteModelForm
    page_title = "Novo Cliente"
    form_title = "Novo Cliente"
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        # adicionar o título da página e o título do formulário ao contexto
        context['page_title'] = self.page_title
        context['form_title'] = self.form_title
        
        return context


