from django.db import models
import os

# Create your models here.
class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key =True) # CPF Ã© Ãºnico para cada cliente Ex: 12345678900
    nome = models.CharField(max_length=100) # Nome do cliente Ex: JoÃ£o da Silva
    data_nascimento = models.DateField() # Data de nascimento do cliente Ex: 21-01-1990
    telefone_whatsapp = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    telefone = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    email = models.EmailField(max_length=100, blank=True, null=True) # Email do cliente Ex:
    
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.cpf}, {self.nome}, {self.data_nascimento}, {self.telefone_whatsapp}, {self.telefone}'  # Retorna o nome do cliente e o CPF do cliente
    
    def get_class_name(self):
        return self.__class__.__name__
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()