from django.core.management.base import BaseCommand
from psqi.models import Questionnaire

class Command(BaseCommand):
    help = 'Remove os testes especificados pelo ID'

    def handle(self, *args, **kwargs):
        ids_to_remove = [28]
        removed_count, _ = Questionnaire.objects.filter(id__in=ids_to_remove).delete()
        self.stdout.write(self.style.SUCCESS(f'Removidos {removed_count} testes com sucesso.'))
