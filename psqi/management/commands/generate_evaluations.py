from django.core.management.base import BaseCommand
from psqi.models import TestScore
from gemini_api.client import get_evaluation

class Command(BaseCommand):
    help = 'Gera avaliações de PSQI para registros existentes que não têm score_evaluation'

    def handle(self, *args, **kwargs):
        registros_sem_avaliacao = TestScore.objects.filter(score_evaluation__isnull=True) | TestScore.objects.filter(score_evaluation='')

        if not registros_sem_avaliacao.exists():
            self.stdout.write(self.style.SUCCESS('Todos os registros já possuem uma avaliação válida.'))
            return

        for registro in registros_sem_avaliacao:
            # Chama a função de avaliação, passando apenas a instância
            avaliacao = get_evaluation(registro.questionnaire)

            # Substituir o campo score_evaluation
            registro.score_evaluation = avaliacao
            registro.save()

            self.stdout.write(self.style.SUCCESS(f'Avaliação gerada para TestScore ID {registro.id}'))

        self.stdout.write(self.style.SUCCESS('Avaliações geradas com sucesso para todos os registros pendentes.'))
