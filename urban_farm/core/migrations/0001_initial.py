# Generated by Django 4.1 on 2024-10-10 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cep', models.CharField(max_length=10)),
                ('endereco', models.CharField(max_length=100)),
                ('complemento', models.CharField(blank=True, max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=2)),
                ('bairro', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel_permissao', models.CharField(choices=[('master', 'Master'), ('colaborador', 'Colaborador')], max_length=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cnpj', models.CharField(max_length=18, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('razao_social', models.CharField(max_length=100)),
                ('nome_fantasia', models.CharField(max_length=100)),
                ('nome_representante', models.CharField(max_length=100)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.endereco')),
            ],
        ),
    ]
