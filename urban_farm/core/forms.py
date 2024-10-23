from django import forms
from django.core.exceptions import ValidationError
from .models import Endereco, Fornecedor, Cliente, Funcionario
import re

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'endereco', 'complemento', 'cidade', 'estado', 'bairro', 'telefone', 'email']

    # Validação do CEP (deve ser numérico e ter 8 dígitos)
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if not re.match(r'^\d{5}-?\d{3}$', cep):  # Aceita '00000-000' ou '00000000'
            raise ValidationError("O CEP deve estar no formato '00000-000'.")
        return cep

    # Validação do telefone (mínimo de 10 caracteres)
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not re.match(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$', telefone):  # Formato: (XX) XXXXX-XXXX
            raise ValidationError("O telefone deve estar no formato '(XX) XXXXX-XXXX'.")
        return telefone

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ('cnpj', 'status', 'razao_social', 'nome_fantasia', 'nome_representante')

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        # Remove formatação
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return cnpj  # Retorna apenas os números

    # Validação da Razão Social (mínimo de 5 caracteres)
    def clean_razao_social(self):
        razao_social = self.cleaned_data.get('razao_social')
        if len(razao_social) < 5:
            raise ValidationError("A razão social deve ter pelo menos 5 caracteres.")
        return razao_social

    # Validação do Nome Fantasia (mínimo de 3 caracteres)
    def clean_nome_fantasia(self):
        nome_fantasia = self.cleaned_data.get('nome_fantasia')
        if len(nome_fantasia) < 3:
            raise ValidationError("O nome fantasia deve ter pelo menos 3 caracteres.")
        return nome_fantasia

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('cpf', 'status', 'nome', 'endereco')

    # Validação do CPF (formato 'XXX.XXX.XXX-XX')
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise ValidationError("O CPF deve estar no formato 'XXX.XXX.XXX-XX'.")
        return cpf

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('cpf', 'nome', 'cargo', 'data_admissao', 'salario', 'status')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise ValidationError("O CPF deve estar no formato 'XXX.XXX.XXX-XX'.")
        return cpf