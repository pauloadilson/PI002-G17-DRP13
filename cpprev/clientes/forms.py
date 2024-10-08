from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from clientes.models import (
    Cliente, 
    RequerimentoInicial, 
    RequerimentoRecurso, 
    Exigencia, 
    EstadoRequerimentoInicial, 
    EstadoRequerimentoRecurso,
    EstadoExigencia,
    ExigenciaRequerimentoInicial,
    ExigenciaRequerimentoRecurso
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Button
from crispy_forms.bootstrap import FormActions

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClienteModelForm, self).__init__(*args, **kwargs)

        # Desabilitar o campo CPF no update
        if self.instance and self.instance.pk:
            self.fields['cpf'].disabled = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cpf', css_class='form-control'),
            Field('nome', css_class='form-control'),
            Field('data_nascimento', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('telefone_whatsapp', css_class='form-control'),
            Field('telefone', css_class='form-control'),
            Field('email', css_class='form-control', type='email'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        clientes = Cliente.objects.all() 
        if len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos')
        if (isinstance(self.instance, Cliente) and Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists()):
            raise forms.ValidationError('CPF já cadastrado')
        return cpf

    def save(self, commit=True):
        return super(ClienteModelForm, self).save(commit=commit)
    
class EscolhaTipoRequerimentoForm(forms.Form):
    TIPO_REQUERIMENTO_CHOICES = [
        ('inicial', 'Requerimento Inicial'),
        ('recurso', 'Requerimento Recurso'),
    ]
    tipo_requerimento = forms.ChoiceField(choices=TIPO_REQUERIMENTO_CHOICES, label="Tipo de Requerimento")
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Field('tipo_requerimento'),
                FormActions(
                    Submit('submit', 'Escolher', css_class='btn btn-primary'),
                    Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
                )
            )

    def save(self, commit=True):
        return super(RequerimentoInicialModelForm, self).save(commit=commit)


class RequerimentoInicialModelForm(forms.ModelForm):
    class Meta:
        model = RequerimentoInicial
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequerimentoInicialModelForm, self).__init__(*args, **kwargs)
        
        # Desabilitar o campo CPF no update
        if self.instance and self.instance.pk:
            self.fields['protocolo'].disabled = True
            self.fields['NB'].disabled = True
            self.fields['requerente_titular'].disabled = True
            self.fields['servico'].disabled = True
        
        self.fields['estado'].queryset = EstadoRequerimentoInicial.objects.all()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('protocolo'),
            Field('NB'),
            Field('requerente_titular'),
            Field('servico'),
            Field('requerente_dependentes'),
            Field('tutor_curador'),
            Field('instituidor'),
            Field('data', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('email', type='email'),
            Field('observacao'),
            Field('estado'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def save(self, commit=True):
        return super(RequerimentoInicialModelForm, self).save(commit=commit)
        
class RequerimentoRecursoModelForm(forms.ModelForm):
    class Meta:
        model = RequerimentoRecurso
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(RequerimentoRecursoModelForm, self).__init__(*args, **kwargs)

        # Desabilitar o campo CPF no update
        if self.instance and self.instance.pk:
            self.fields['protocolo'].disabled = True
            self.fields['NB'].disabled = True
            self.fields['requerente_titular'].disabled = True
            self.fields['servico'].disabled = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('protocolo'),
            Field('NB'),
            Field('requerente_titular'),
            Field('servico'),
            Field('requerente_dependentes'),
            Field('tutor_curador'),
            Field('instituidor'),
            Field('data', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('email', type='email'),
            Field('observacao'),
            Field('estado'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

        def save(self, commit=True):
            return super(RequerimentoRecursoModelForm, self).save(commit=commit)

class ExigenciaModelForm(forms.ModelForm):
    class Meta:
        model = Exigencia
        fields = ('requerimento', 'data', 'natureza', 'estado')

    def __init__(self, *args, **kwargs):
        super(ExigenciaModelForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = EstadoExigencia.objects.all()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('requerimento', css_class='form-control', type='hidden'),
            Field('data', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('natureza', css_class='form-control'),
            Field('estado', css_class='form-control'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def save(self, commit=True):
        return super(ExigenciaModelForm, self).save(commit=commit)
    

class ExigenciaRequerimentoInicialModelForm(ExigenciaModelForm):
    class Meta:
        model = ExigenciaRequerimentoInicial
        fields = ('requerimento', 'data', 'natureza', 'estado')

class ExigenciaRequerimentoRecursoModelForm(ExigenciaModelForm):
    class Meta:
        model = ExigenciaRequerimentoRecurso
        fields = ('requerimento', 'data', 'natureza', 'estado')

# Formulário personalizado para EstadoRequerimentoInicial
class EstadoRequerimentoInicialForm(forms.ModelForm):
    class Meta:
        model = EstadoRequerimentoInicial
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].choices = EstadoRequerimentoInicial().get_estados()

# Formulário personalizado para EstadoRequerimentoRecurso
class EstadoRequerimentoRecursoForm(forms.ModelForm):
    class Meta:
        model = EstadoRequerimentoRecurso
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].choices = EstadoRequerimentoRecurso().get_estados()