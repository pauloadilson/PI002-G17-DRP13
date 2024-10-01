from django.http import Http404
from django.db.models.base import Model as Model
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.views.generic.edit import FormView
from clientes.models import (
    Cliente, 
    RequerimentoInicial, 
    RequerimentoRecurso, 
    ExigenciaRequerimentoInicial,
    ExigenciaRequerimentoRecurso,
    EstadoRequerimentoRecurso
)
from clientes.forms import (
    ClienteModelForm, 
    EscolhaTipoRequerimentoForm, 
    RequerimentoInicialModelForm, 
    RequerimentoRecursoModelForm, 
    ExigenciaRequerimentoInicialModelForm,
    ExigenciaRequerimentoRecursoModelForm
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
#from datetime import datetime, timedelta

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    title = "Página inicial"

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context

class ClientesListView(ListView):
    model = Cliente
    template_name = "clientes.html"
    context_object_name = "clientes"
    title = "Clientes"
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
        context["title"] = self.title
        return context

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'form.html'
    form_class = ClienteModelForm
    title = "Novo Cliente"
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        # adicionar o título da página e o título do formulário ao contexto
        context['title'] = self.title
        
        return context

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "cliente.html"
    context_object_name = "cliente"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        cliente_id = self.object.cpf
        title = f"Cliente {cliente_id}"
        requerimentos_cliente = RequerimentoInicial.objects.filter(is_deleted=False).filter(
            requerente_titular__cpf__icontains=cliente_id
        )
        recursos_cliente = RequerimentoRecurso.objects.filter(is_deleted=False).filter(
            requerente_titular__cpf__icontains=cliente_id
        )
        qtde_instancias_filhas = self.object.total_requerimentos

        context["title"] = title
        context["requerimentos_cliente"] = requerimentos_cliente
        context["recursos_cliente"] = recursos_cliente
        context["qtde_instancias_filhas"] = qtde_instancias_filhas

        return context

class EscolherTipoRequerimentoView(FormView):
    template_name = 'form.html'
    title = "Escolher Tipo de Requerimento"
    form_class = EscolhaTipoRequerimentoForm
    success_url = reverse_lazy('escolher_tipo_requerimento')

    def form_valid(self, form):
        tipo = form.cleaned_data['tipo_requerimento']
        cpf = cpf = self.kwargs['cpf']  # Obtendo o CPF do formulário

        # Incluindo o CPF na URL de redirecionamento
        if tipo == 'inicial':
            return redirect('adicionar_requerimento_inicial', cpf=cpf)
        elif tipo == 'recurso':
            return redirect('adicionar_requerimento_recurso', cpf=cpf)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(EscolherTipoRequerimentoView, self).get_context_data(**kwargs)
        # adicionar o título da página e o título do formulário ao contexto
        context['title'] = self.title
        
        return context
    
class RequerimentoInicialCreateView(CreateView):
    model = RequerimentoInicial
    form_class = RequerimentoInicialModelForm
    template_name = 'form.html'
    title = "Novo Requerimento"
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        # Filtra o cliente titular do requerimento se is_deleted=False
        initial["requerente_titular"] = Cliente.objects.filter(is_deleted=False).get(cpf=self.kwargs["cpf"])
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os clientes com is_deleted=False para os campos tutor_curador e instituidor
        form.fields['tutor_curador'].queryset = Cliente.objects.filter(is_deleted=False)
        form.fields['instituidor'].queryset = Cliente.objects.filter(is_deleted=False)
        return form

    def form_valid(self, form):
        form.instance.requerente_titular = Cliente.objects.filter(is_deleted=False).get(cpf=self.kwargs["cpf"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento_inicial",kwargs={"cpf":self.kwargs["cpf"],"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(RequerimentoInicialCreateView, self).get_context_data(**kwargs)
        context["title"] = self.title
        context["form_title_identificador"] = f'CPF nº {self.kwargs["cpf"]}'
        return context
    
class RequerimentoRecursoCreateView(CreateView):
    model = RequerimentoRecurso
    form_class = RequerimentoRecursoModelForm
    template_name = 'form.html'
    title = "Novo Recurso"
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        # Filtra o cliente titular do requerimento se is_deleted=False
        initial["requerente_titular"] = Cliente.objects.filter(is_deleted=False).get(cpf=self.kwargs["cpf"])
        return initial
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os clientes com is_deleted=False para os campos tutor_curador e instituidor
        form.fields['tutor_curador'].queryset = Cliente.objects.filter(is_deleted=False)
        form.fields['instituidor'].queryset = Cliente.objects.filter(is_deleted=False)
        return form

    def form_valid(self, form):
        form.instance.requerente_titular = Cliente.objects.filter(is_deleted=False).get(cpf=self.kwargs["cpf"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento_recurso",kwargs={"cpf":self.kwargs["cpf"],"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(RequerimentoRecursoCreateView, self).get_context_data(**kwargs)
        context["title"] = self.title
        context["form_title_identificador"] = f'CPF nº {self.kwargs["cpf"]}'
        return context
    
class RequerimentoInicialDetailView(DetailView):
    model = RequerimentoInicial
    template_name = "requerimento.html"
    context_object_name = "requerimento"
    title = "Requerimento"
    paginate_by = 10

    cliente_id = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj

    def get_context_data(self, **kwargs):
        context = super(RequerimentoInicialDetailView, self).get_context_data(**kwargs)

        cliente_id = self.object.requerente_titular.cpf
        cliente = Cliente.objects.filter(is_deleted=False).filter(cpf__icontains=cliente_id)[
            0
        ]  # .order_by('nome') '-nome' para ordem decrescente
        exigencias_requerimento = self.object.requerimento_exigencia.filter(is_deleted=False).filter(requerimento__id=self.object.id)
        qtde_instancias_filhas = self.object.total_exigencias

        context["title"] = self.title
        context["cliente"] = cliente
        context["exigencias_requerimento"] = exigencias_requerimento
        context["qtde_instancias_filhas"] = qtde_instancias_filhas
        return context

class RequerimentoRecursoDetailView(DetailView):
    model = RequerimentoRecurso
    template_name = "requerimento.html"
    context_object_name = "requerimento"
    title = "Recurso"
    paginate_by = 10

    cliente_id = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Recurso não encontrado")
        return obj

    def get_context_data(self, **kwargs):
        context = super(RequerimentoRecursoDetailView, self).get_context_data(**kwargs)

        cliente_id = self.object.requerente_titular.cpf
        cliente = Cliente.objects.filter(is_deleted=False).filter(cpf__icontains=cliente_id)[
            0
        ]  # .order_by('nome') '-nome' para ordem decrescente
        exigencias_requerimento = self.object.requerimento_exigencia.filter(is_deleted=False).filter(requerimento__id=self.object.id)
        qtde_instancias_filhas = self.object.total_exigencias

        context["title"] = self.title
        context["cliente"] = cliente
        context["exigencias_requerimento"] = exigencias_requerimento
        context["qtde_instancias_filhas"] = qtde_instancias_filhas
        return context
    
class ExigenciaRequerimentoInicialCreateView(CreateView):
    model = ExigenciaRequerimentoInicial
    template_name = "form.html"
    form_class = ExigenciaRequerimentoInicialModelForm
    title = "Nova Exigência"
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        initial["requerimento"] = RequerimentoInicial.objects.filter(is_deleted=False).get(id=self.kwargs["pk"])
        return initial

    def form_valid(self, form):
        form.instance.requerimento = RequerimentoInicial.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento_inicial", kwargs={"cpf":self.kwargs["cpf"],"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(ExigenciaRequerimentoInicialCreateView, self).get_context_data(**kwargs)
        context["title"] = self.title
        context["form_title_identificador"] = f'Id nº {self.kwargs["pk"]}'
        return context

class ExigenciaRequerimentoRecursoCreateView(CreateView):
    model = ExigenciaRequerimentoRecurso
    template_name = "form.html"
    form_class = ExigenciaRequerimentoRecursoModelForm
    title = "Nova Exigência"
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        initial["requerimento"] = RequerimentoRecurso.objects.filter(is_deleted=False).get(id=self.kwargs["pk"])
        return initial

    def form_valid(self, form):
        form.instance.requerimento = RequerimentoRecurso.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento_recurso", kwargs={"cpf":self.kwargs["cpf"],"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(ExigenciaRequerimentoRecursoCreateView, self).get_context_data(**kwargs)
        context["title"] = self.title
        context["form_title_identificador"] = f'Id nº {self.kwargs["pk"]}'
        return context