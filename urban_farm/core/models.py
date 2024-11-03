# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nivel_permissao = models.CharField(max_length=12, choices=[('master', 'Master'), ('colaborador', 'Colaborador')])
class Monitoramento(models.Model):
    pedidos = models.IntegerField()
    plantas = models.IntegerField()
    coletas = models.IntegerField()
    kg_colheita = models.FloatField()
    temperatura_ar = models.FloatField()
    quantidade_agua = models.FloatField()
    valor_ph = models.FloatField()
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()

class Pedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_pedido = models.DateTimeField(auto_now_add=True)

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=10)
    endereco = models.CharField(max_length=100)
    complemento = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    bairro = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

class Fornecedor(models.Model):
    id = models.AutoField(primary_key=True)
    # cnpj é CharField pois é mais facil validar e se deixar "IntegerField" ele remove 0 a esquerda
    cnpj = models.CharField(max_length=18, unique=True)
    status = models.BooleanField(default=True)
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    nome_representante = models.CharField(max_length=100)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PF')  # Adiciona default='PF'
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    status = models.BooleanField(default=True)
    nome = models.CharField(max_length=100, blank=True)  # Permitir vazio
    razao_social = models.CharField(max_length=100, null=True, blank=True)  # Para PJ
    nome_fantasia = models.CharField(max_length=100, null=True, blank=True)  # Para PJ
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validação para Pessoa Física
        if self.tipo == 'PF':
            if not self.cpf:
                raise ValidationError('CPF é obrigatório para Pessoa Física')
            if self.cnpj:
                raise ValidationError('CNPJ não deve ser preenchido para Pessoa Física')
            if self.razao_social or self.nome_fantasia:
                raise ValidationError('Razão Social e Nome Fantasia não devem ser preenchidos para Pessoa Física')

        # Validação para Pessoa Jurídica
        if self.tipo == 'PJ':
            if not self.cnpj:
                raise ValidationError('CNPJ é obrigatório para Pessoa Jurídica')
            if self.cpf:
                raise ValidationError('CPF não deve ser preenchido para Pessoa Jurídica')
            if not self.razao_social or not self.nome_fantasia:
                raise ValidationError('Razão Social e Nome Fantasia são obrigatórios para Pessoa Jurídica')

    def __str__(self):
        if self.tipo == 'PF':
            return f"{self.nome} (CPF: {self.cpf})"
        return f"{self.nome_fantasia} (CNPJ: {self.cnpj})"

class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)
    status = models.BooleanField(default=True)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50, default='Funcionario')
    data_admissao = models.DateField(default=timezone.now)
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

from django.db import models

class Planta(models.Model):
    ESTAGIOS_PLANTIO = [
        ('GERMINACAO', 'Germinação'),
        ('PLANTULA', 'Plântula'),
        ('VEGETATIVO', 'Vegetativo'),
        ('FLORACAO', 'Floração'),
        ('FRUTIFICACAO', 'Frutificação'),
        ('COLHEITA', 'Colheita'),
    ]

    nome = models.CharField(max_length=100)
    data_plantio = models.DateField()
    quantidade_plantada = models.DecimalField(max_digits=10, decimal_places=2)  # Quantidade em kg
    estagio = models.CharField(max_length=20, choices=ESTAGIOS_PLANTIO)
    data_colheita_estimada = models.DateField(null=True, blank=True)  # Pode ser preenchida posteriormente

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'
        ordering = ['data_plantio']  # Ordena pela data de plantio
