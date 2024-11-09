from django import forms
from django.core.exceptions import ValidationError
from .models import Endereco, Fornecedor, Cliente, Funcionario,Venda, ItemVenda
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

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('cpf', 'nome', 'cargo', 'data_admissao', 'salario', 'status')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise ValidationError("O CPF deve estar no formato 'XXX.XXX.XXX-XX'.")
        return cpf

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('tipo', 'cpf', 'cnpj', 'nome', 'razao_social', 'nome_fantasia', 'status')

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cpf = cleaned_data.get('cpf')
        cnpj = cleaned_data.get('cnpj')
        razao_social = cleaned_data.get('razao_social')
        nome_fantasia = cleaned_data.get('nome_fantasia')

        if tipo == 'PF':
            if not cpf:
                raise forms.ValidationError('CPF é obrigatório para Pessoa Física')
            if cnpj:
                raise forms.ValidationError('CNPJ não deve ser preenchido para Pessoa Física')
            if razao_social or nome_fantasia:
                raise forms.ValidationError('Razão Social e Nome Fantasia não devem ser preenchidos para Pessoa Física')

        elif tipo == 'PJ':
            if not cnpj:
                raise forms.ValidationError('CNPJ é obrigatório para Pessoa Jurídica')
            if cpf:
                raise forms.ValidationError('CPF não deve ser preenchido para Pessoa Jurídica')
            if not razao_social or not nome_fantasia:
                raise forms.ValidationError('Razão Social e Nome Fantasia são obrigatórios para Pessoa Jurídica')

        return cleaned_data

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ('item', 'quantidade', 'valor_unitario')

    def clean(self):
        cleaned_data = super().clean()
        quantidade = cleaned_data.get('quantidade')
        valor_unitario = cleaned_data.get('valor_unitario')

        if quantidade <= 0:
            raise forms.ValidationError('A quantidade deve ser maior que zero.')
        if valor_unitario <= 0:
            raise forms.ValidationError('O valor unitário deve ser maior que zero.')

        return cleaned_data

class VendaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True)
    
    # Campos para itens de venda
    item = forms.CharField(max_length=100, required=False)
    quantidade = forms.IntegerField(min_value=1, required=False)
    valor_unitario = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Venda
        fields = ('cliente', 'preco_total', 'item', 'quantidade', 'valor_unitario')

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        preco_total = cleaned_data.get('preco_total')

        if not cliente:
            raise forms.ValidationError('O cliente é obrigatório.')
        if preco_total <= 0:
            raise forms.ValidationError('O preço total deve ser maior que zero.')

        return cleaned_data