from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from clientes.views import (
    IndexView,
    ClientesListView,
    ClienteCreateView,
    ClienteDetailView,
    ClienteUpdateView,
    ClienteDeleteView,
    RequerimentoInicialCreateView,
    RequerimentoInicialDetailView,
    RequerimentoInicialUpdateView,
    RequerimentoInicialDeleteView,
    RequerimentoRecursoCreateView,
    RequerimentoRecursoDetailView,
    RequerimentoRecursoUpdateView,
    RequerimentoRecursoDeleteView,
    ExigenciaRequerimentoInicialCreateView,
    ExigenciaRequerimentoInicialUpdateView,
    ExigenciaRequerimentoInicialDeleteView,
    ExigenciaRequerimentoRecursoCreateView,
    ExigenciaRequerimentoRecursoUpdateView,
    ExigenciaRequerimentoRecursoDeleteView,
    EscolherTipoRequerimentoView
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("clientes/", ClientesListView.as_view(), name="clientes"),
    path("cliente/", include ([
        path('adicionar', ClienteCreateView.as_view(), name='adicionar_cliente'),
        path('<int:pk>', ClienteDetailView.as_view(), name='cliente'),
        path('<int:pk>/atualizar', ClienteUpdateView.as_view(), name='atualizar_cliente'),
        path('<int:pk>/excluir', ClienteDeleteView.as_view(), name='excluir_cliente'),
    ])),
    path('escolher-requerimento/<str:cpf>', EscolherTipoRequerimentoView.as_view(), name='escolher_tipo_requerimento'),
    path("requerimento_inicial/<int:cpf>/", include ([
            path("adicionar", RequerimentoInicialCreateView.as_view(), name="adicionar_requerimento_inicial"),
            path("<int:pk>", RequerimentoInicialDetailView.as_view(), name="requerimento_inicial"),
            path("<int:pk>/atualizar", RequerimentoInicialUpdateView.as_view(), name="atualizar_requerimento_inicial"),
            path("<int:pk>/excluir", RequerimentoInicialDeleteView.as_view(), name="excluir_requerimento_inicial"),
            
    ])),
    path("requerimento_recurso/<int:cpf>/", include ([
            path("adicionar", RequerimentoRecursoCreateView.as_view(), name="adicionar_requerimento_recurso"),
            path("<int:pk>", RequerimentoRecursoDetailView.as_view(), name="requerimento_recurso"),
            path("<int:pk>/atualizar", RequerimentoRecursoUpdateView.as_view(), name="atualizar_requerimento_recurso"),
            path("<int:pk>/excluir", RequerimentoRecursoDeleteView.as_view(), name="excluir_requerimento_recurso"),
    ])),
    path("exigencia_requerimento_inicial/<int:cpf>/<int:pk>/", include ([
            path("adicionar", ExigenciaRequerimentoInicialCreateView.as_view(), name="adicionar_exigencia_requerimento_inicial"),
            path("atualizar", ExigenciaRequerimentoInicialUpdateView.as_view(), name="atualizar_exigencia_requerimento_inicial"),
            path("excluir", ExigenciaRequerimentoInicialDeleteView.as_view(), name="excluir_exigencia_requerimento_inicial"),
    ])),
    path("exigencia_requerimento_recurso/<int:cpf>/<int:pk>/", include ([
            path("adicionar", ExigenciaRequerimentoRecursoCreateView.as_view(), name="adicionar_exigencia_requerimento_recurso"),
            path("atualizar", ExigenciaRequerimentoRecursoUpdateView.as_view(), name="atualizar_exigencia_requerimento_recurso"),
            path("excluir", ExigenciaRequerimentoRecursoDeleteView.as_view(), name="excluir_exigencia_requerimento_recurso"),
    ])),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
