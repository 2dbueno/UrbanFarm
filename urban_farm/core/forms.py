from django import forms
from .models import Endereco, Fornecedor, Cliente, Funcionario

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'endereco', 'complemento', 'cidade', 'estado', 'bairro', 'telefone', 'email']

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ('cnpj', 'status', 'razao_social', 'nome_fantasia', 'nome_representante')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('cpf', 'status', 'nome', 'endereco')

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('cpf', 'status', 'nome', 'endereco')