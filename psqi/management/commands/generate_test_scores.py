from django.core.management.base import BaseCommand
from psqi.models import Questionnaire, TestScore

class Command(BaseCommand):
    help = 'Gera TestScores para Questionnaires existentes'

    def handle(self, *args, **kwargs):
        questionnaires = Questionnaire.objects.all()
        for questionnaire in questionnaires:
            test_score, created = TestScore.objects.get_or_create(questionnaire=questionnaire)
            test_score.save()
            self.stdout.write(self.style.SUCCESS(f"{'Criado' if created else 'Atualizado'} TestScore para {questionnaire} com score {test_score.total_score}"))
