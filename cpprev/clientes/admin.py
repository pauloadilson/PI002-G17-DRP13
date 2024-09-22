from django.contrib import admin
from .models import Cliente

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome', 'data_nascimento', 'telefone_whatsapp', 'telefone', 'email', 'is_deleted')
    search_fields = ('cpf', 'nome')

admin.site.register(Cliente, ClienteAdmin) # Registra o modelo Cliente no admin do Django da Classe Cliente e da configuração ClienteAdmin
