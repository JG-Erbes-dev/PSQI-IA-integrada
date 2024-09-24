from django.core.management.base import BaseCommand
from psqi.models import Questionnaire

class Command(BaseCommand):
    help = 'Insere um motivo na tabela questionnaire em um ID específico'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='ID do registro a ser inserido ou atualizado')
        parser.add_argument('other_reason', type=str, help='Motivo a ser inserido')

    def handle(self, *args, **kwargs):
        record_id = kwargs['id']
        other_reason = kwargs['other_reason']

        # Tenta obter o registro existente
        try:
            questionnaire = Questionnaire.objects.get(id=record_id)
            questionnaire.other_reasons = other_reason  # Atualiza o campo
            questionnaire.save()
            self.stdout.write(self.style.SUCCESS(f'Motivo atualizado para o registro ID {record_id}: "{other_reason}".'))
        except Questionnaire.DoesNotExist:
            # Se o registro não existir, cria um novo com o ID especificado
            questionnaire = Questionnaire(id=record_id, other_reasons=other_reason)
            questionnaire.save()
            self.stdout.write(self.style.SUCCESS(f'Registro ID {record_id} criado com motivo: "{other_reason}".'))
