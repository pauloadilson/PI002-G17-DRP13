from django.contrib import admin
# from .models import Cliente, RequerimentoInicial, RequerimentoRecurso, Estado, EstadoRequerimentoInicial, EstadoRequerimentoRecurso,  HistoricoEstadoRequerimento, Servico, Exigencia, Natureza, EstadoExigencia, HistoricoEstadoExigencia
# user session
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date', 'session_data' )
    search_fields = ('session_key', 'session_data')
    list_filter = ('expire_date',)