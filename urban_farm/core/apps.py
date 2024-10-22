from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .models import Planta
        # Verifica se já existem plantas cadastradas
        if not Planta.objects.exists():
            # Adiciona dados iniciais
            Planta.objects.bulk_create([
                Planta(nome='Tomate', data_plantio='2024-01-01', quantidade_plantada=10, estagio='GERMINACAO', data_colheita_estimada='2024-03-01'),
                Planta(nome='Alface', data_plantio='2024-01-15', quantidade_plantada=5, estagio='PLANTULA', data_colheita_estimada='2024-03-15'),
                Planta(nome='Cenoura', data_plantio='2024-01-20', quantidade_plantada=8, estagio='VEGETATIVO', data_colheita_estimada='2024-04-20'),
                Planta(nome='Bergamota', data_plantio='2024-02-01', quantidade_plantada=12, estagio='FRUTIFICACAO', data_colheita_estimada='2024-06-01'),
                Planta(nome='Rúcula', data_plantio='2024-02-10', quantidade_plantada=6, estagio='COLHEITA', data_colheita_estimada='2024-03-10'),
                Planta(nome='Espinafre', data_plantio='2024-01-05', quantidade_plantada=7, estagio='GERMINACAO', data_colheita_estimada='2024-02-15'),
                Planta(nome='Brócolis', data_plantio='2024-01-25', quantidade_plantada=4, estagio='PLANTULA', data_colheita_estimada='2024-03-30'),
                Planta(nome='Pimentão', data_plantio='2024-02-05', quantidade_plantada=9, estagio='VEGETATIVO', data_colheita_estimada='2024-05-05'),
                Planta(nome='Cebola', data_plantio='2024-02-15', quantidade_plantada=15, estagio='FRUTIFICACAO', data_colheita_estimada='2024-06-15'),
                Planta(nome='Batata', data_plantio='2024-02-20', quantidade_plantada=20, estagio='COLHEITA', data_colheita_estimada='2024-07-01'),
                Planta(nome='Basilicão', data_plantio='2024-02-25', quantidade_plantada=10, estagio='GERMINACAO', data_colheita_estimada='2024-03-25'),
                Planta(nome='Salsa', data_plantio='2024-03-01', quantidade_plantada=5, estagio='PLANTULA', data_colheita_estimada='2024-04-10'),
                Planta(nome='Coentro', data_plantio='2024-03-05', quantidade_plantada=8, estagio='VEGETATIVO', data_colheita_estimada='2024-05-15'),
                Planta(nome='Pepino', data_plantio='2024-03-10', quantidade_plantada=11, estagio='FRUTIFICACAO', data_colheita_estimada='2024-06-20'),
                Planta(nome='Abobrinha', data_plantio='2024-03-15', quantidade_plantada=14, estagio='COLHEITA', data_colheita_estimada='2024-06-30'),
                Planta(nome='Couve', data_plantio='2024-03-20', quantidade_plantada=6, estagio='GERMINACAO', data_colheita_estimada='2024-04-25'),
                Planta(nome='Milho', data_plantio='2024-03-25', quantidade_plantada=30, estagio='PLANTULA', data_colheita_estimada='2024-08-15'),
                Planta(nome='Feijão', data_plantio='2024-04-01', quantidade_plantada=25, estagio='VEGETATIVO', data_colheita_estimada='2024-07-01'),
                Planta(nome='Morango', data_plantio='2024-04-05', quantidade_plantada=12, estagio='FRUTIFICACAO', data_colheita_estimada='2024-07-10'),
                Planta(nome='Framboesa', data_plantio='2024-04-10', quantidade_plantada=15, estagio='COLHEITA', data_colheita_estimada='2024-08-01')

            ])
