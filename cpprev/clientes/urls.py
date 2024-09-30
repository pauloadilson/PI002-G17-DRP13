from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from clientes.views import (
    IndexView,
    ClientesListView,
    ClienteCreateView,
    ClienteDetailView,
    RequerimentoInicialCreateView,
    RequerimentoRecursoCreateView,
    RequerimentoInicialDetailView,
    RequerimentoRecursoDetailView,
    ExigenciaRequerimentoInicialCreateView,
    ExigenciaRequerimentoRecursoCreateView,
    EscolherTipoRequerimentoView
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("clientes/", ClientesListView.as_view(), name="clientes"),
    path("novo_cliente/", ClienteCreateView.as_view(), name="novo_cliente"),
    path("cliente/<int:pk>", ClienteDetailView.as_view(), name="cliente"),
    path('escolher-requerimento/<str:cpf>', EscolherTipoRequerimentoView.as_view(), name='escolher_tipo_requerimento'),
    path("requerimento_inicial/<int:cpf>/incluir", RequerimentoInicialCreateView.as_view(), name="novo_requerimento_inicial"),
    path("requerimento_recurso/<int:cpf>/incluir", RequerimentoRecursoCreateView.as_view(), name="novo_requerimento_recurso"),
    path("requerimento_inicial/<int:cpf>/<int:pk>", RequerimentoInicialDetailView.as_view(), name="requerimento_inicial"),
    path("requerimento_recurso/<int:cpf>/<int:pk>", RequerimentoRecursoDetailView.as_view(), name="requerimento_recurso"),
    path("exigencia_requerimento_inicial/<int:cpf>/<int:pk>/incluir", ExigenciaRequerimentoInicialCreateView.as_view(), name="nova_exigencia_requerimento_inicial"),
    path("exigencia_requerimento_recurso/<int:cpf>/<int:pk>/incluir", ExigenciaRequerimentoRecursoCreateView.as_view(), name="nova_exigencia_requerimento_recurso"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
