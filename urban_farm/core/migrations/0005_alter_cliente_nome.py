# Generated by Django 4.2.16 on 2024-11-08 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_cliente_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
