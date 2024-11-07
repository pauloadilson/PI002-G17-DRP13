import datetime
from django.db import models

# Create your models here.
class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key =True) # CPF e unico para cada cliente Ex: 12345678900
    nome = models.CharField(max_length=100) # Nome do cliente Ex: Joao da Silva
    data_nascimento = models.DateField() # Data de nascimento do cliente Ex: 21-01-1990
    telefone = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    observacao_telefone = models.TextField(blank=True, null=True) # Observacao do telefone do cliente Ex: Recado Luiz
    telefone_whatsapp = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    email = models.EmailField(max_length=100, blank=True, null=True) # Email do cliente Ex:
    
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.cpf}, {self.nome}, {self.data_nascimento}, {self.telefone_whatsapp}, {self.telefone}, {self.email}'  # Retorna o nome do cliente e o CPF do cliente
    
    def get_class_name(self):
        return self.__class__.__name__
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    @property
    def total_requerimentos(self):
        lista_requerimentos = Requerimento.objects.filter(is_deleted=False).filter(
            requerente_titular=self
            )
        return len(lista_requerimentos)

class Servico(models.Model):
    id = models.AutoField(primary_key=True) # ID do serviço
    nome = models.CharField(max_length=100) # Nome do serviço Ex: Aposentadoria por idade, Aposentadoria por invalidez

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do serviço
    
class Requerimento(models.Model):
    id = models.AutoField(primary_key=True) # ID do requerimento
    protocolo = models.CharField(max_length=20, unique=True) # Protocolo do requerimento
    NB = models.CharField(max_length=20, blank=True, null=True) # Numero do benefi­cio do cliente
    requerente_titular = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_titular_requerimento') # Relacionamento com o modelo Cliente
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='servico_requerimento') # Servico solicitado Ex: Aposentadoria por idade
    requerente_dependentes = models.TextField(blank=True, null=True) #.ManyToManyField(Cliente, related_name='cliente_dependente_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    tutor_curador = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_tutor_curador_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    instituidor = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_instituidor_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    data = models.DateField() # Data do requerimento
    email = models.EmailField(max_length=100, blank=True, null=True) # Email do requerente na data do requerimento. Não atualiza o cadastrado no cliente
    observacao = models.TextField(blank=True, null=True) # Observacoes do requerimento

    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Requerimento de NB nº {self.NB} para {self.servico.nome}: {self.requerente_titular.nome}, {self.requerente_titular.cpf}, {self.requerente_titular.data_nascimento}' # Retorna o nome do cliente e a data do requerimento

    def get_class_name(self):
        return self.__class__.__name__
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
    
    def get_class_name(self):
        return self.__class__.__name__
    
class EstadoRequerimentoInicial(models.Model):
    ESTADOS_INICIAIS = [
        ('em análise', 'Em Análise'),
        ('concluído deferido', 'Concluído Deferido'),
        ('concluído indeferido', 'Concluído Indeferido'),
    ]
    
    id = models.AutoField(primary_key=True) # ID do estado
    nome = models.CharField(max_length=100,choices=ESTADOS_INICIAIS) # Nome do estado Ex: Em exigencia, Em analise, Conclui­do

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do estado

class RequerimentoInicial(Requerimento):
    estado = models.ForeignKey(EstadoRequerimentoInicial, on_delete=models.PROTECT, related_name='estado_requerimento_inicial') # Estado do requerimento Ex: Pendente, Concluido

    @property
    def total_exigencias(self):
        lista_exigencias = ExigenciaRequerimentoInicial.objects.filter(is_deleted=False).filter(
            requerimento=self
            )
        return len(lista_exigencias)
    
    @property
    def total_mudancas_estado(self):
        lista_mudancas_estado = HistoricoMudancaEstadoRequerimentoInicial.objects.filter(requerimento=self)
        return len(lista_mudancas_estado)

class EstadoRequerimentoRecurso(models.Model):
    ESTADOS_RECURSOS = [
        ('em análise na junta', 'Em Análise na Junta'),
        ('em análise no conselho', 'Em Análise no Conselho'),
        ('concluído', 'Concluído'),
    ]

    id = models.AutoField(primary_key=True) # ID do estado
    nome = models.CharField(max_length=30, choices=ESTADOS_RECURSOS)
    
    def __str__(self) -> str:
        return f'{self.nome}'

class RequerimentoRecurso(Requerimento):
    estado = models.ForeignKey(EstadoRequerimentoRecurso, on_delete=models.PROTECT, related_name='estado_requerimento_recurso') # Estado do requerimento Ex: Em analise, Concluido
    
    @property
    def total_exigencias(self):
        lista_exigencias = ExigenciaRequerimentoRecurso.objects.filter(is_deleted=False).filter(
            requerimento=self
            )
        return len(lista_exigencias)
class EstadoExigencia(models.Model):
    ESTADOS_EXIGENCIA = [
        ('em análise', 'Em Análise'),
        ('concluído', 'Concluído'),
    ]
    
    id = models.AutoField(primary_key=True) # ID do estado
    nome = models.CharField(max_length=100,choices=ESTADOS_EXIGENCIA) # Nome do estado Ex: Em exigencia, Em analise, Conclui­do

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do estado
    
class Natureza(models.Model):
    id = models.AutoField(primary_key=True) # ID da natureza
    nome = models.CharField(max_length=100) # Nome da natureza Ex: Documentacao, Informacao

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome da natureza
    
class Exigencia(models.Model):
    id = models.AutoField(primary_key=True) # ID da exigÃªncia
    requerimento = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='requerimento_exigencia') # Relacionamento com o modelo Requerimento
    data = models.DateField() # Data da exigÃªncia
    natureza = models.ForeignKey(Natureza, on_delete=models.PROTECT, related_name='natureza_exigencia') # Natureza da exigecia Ex: Documentacao, Informacao
    estado = models.ForeignKey(EstadoExigencia, on_delete=models.PROTECT, related_name='estado_exigencia') # Estado do recurso Ex: Pendente, Conclui­do
    
    is_deleted = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f'Exigência: id nº {self.id} do NB nº {self.requerimento.NB} de {self.requerimento.requerente_titular.nome}, {self.requerimento.requerente_titular.cpf}'
    
    def get_class_name(self):
        return self.__class__.__name__
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class ExigenciaRequerimentoInicial(Exigencia):
    # herdar de Exigencia
    pass

class ExigenciaRequerimentoRecurso(Exigencia):
    # herdar de Exigencia
    pass

class Atendimento(models.Model):
    id = models.AutoField(primary_key=True) # ID do atendimento
    data = models.DateTimeField() # Data do atendimento
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_atendimento') # Relacionamento com o modelo Cliente
    requerimento = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='requerimento_atendimento', blank=True, null=True) # Relacionamento com o modelo Requerimento
    descricao = models.TextField(blank=True, null=True) # Descricao do atendimento
    observacao = models.TextField(blank=True, null=True) # Observacao do atendimento

    is_deleted = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Atendimento: id nº {self.id} de {self.cliente.nome}, {self.cliente.cpf}' # Retorna o nome do atendimento

class Documento(models.Model):
    id = models.AutoField(primary_key=True) # ID do documento
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_documento') # Relacionamento com o modelo Cliente
    arquivo = models.FileField(upload_to='documentos/') # Arquivo do documento
    nome_arquivo = models.CharField(max_length=100) # Nome do documento Ex: RG, CPF, Comprovante de residencia
    descricao = models.TextField(blank=True, null=True) # Descricao do documento
    requerimento = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='requerimento_documento', blank=True, null=True) # Relacionamento com o modelo Requerimento
    exigencia = models.ForeignKey(Exigencia, on_delete=models.PROTECT, related_name='exigencia_documento', blank=True, null=True) # Relacionamento com o modelo Exigencia

    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.nome_arquivo}' # Retorna o nome do documento
    

class HistoricoMudancaEstadoRequerimentoInicial(models.Model):
    id = models.AutoField(primary_key=True) # ID do historico de estado do requerimento
    requerimento = models.ForeignKey(RequerimentoInicial, on_delete=models.PROTECT, related_name='historico_estado_requerimento')
    estado_anterior = models.ForeignKey(EstadoRequerimentoInicial, on_delete=models.SET_NULL, null=True, related_name='estado_anterior')
    estado_novo = models.ForeignKey(EstadoRequerimentoInicial, on_delete=models.PROTECT, related_name='estado_novo')
    observacao = models.TextField(blank=True, null=True)
    data_mudanca = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requerimento.protocolo} do estado {self.estado_anterior.nome} para {self.estado_novo.nome} em {self.data_mudanca}"
    