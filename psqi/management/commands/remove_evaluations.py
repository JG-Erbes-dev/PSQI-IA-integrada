from django.core.management.base import BaseCommand
from psqi.models import TestScore

class Command(BaseCommand):
    help = 'Remove avaliações do PSQI'

    def handle(self, *args, **kwargs):
        TestScore.objects.all().update(score_evaluation='')
        self.stdout.write(self.style.SUCCESS('Todas as avaliações foram removidas com sucesso.'))