# Generated by Django 4.1 on 2024-10-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_plantio', models.DateField()),
                ('quantidade_plantada', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estagio', models.CharField(choices=[('GERMINACAO', 'Germinação'), ('PLANTULA', 'Plântula'), ('VEGETATIVO', 'Vegetativo'), ('FLORACAO', 'Floração'), ('FRUTIFICACAO', 'Frutificação'), ('COLHEITA', 'Colheita')], max_length=20)),
                ('data_colheita_estimada', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Planta',
                'verbose_name_plural': 'Plantas',
                'ordering': ['data_plantio'],
            },
        ),
    ]
