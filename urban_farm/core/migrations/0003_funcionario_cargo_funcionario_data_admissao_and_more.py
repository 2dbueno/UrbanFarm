# Generated by Django 4.1 on 2024-10-23 17:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_planta'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='cargo',
            field=models.CharField(default='Não informado', max_length=50),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='data_admissao',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='salario',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]