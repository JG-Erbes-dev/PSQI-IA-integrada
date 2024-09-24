from django.core.management.base import BaseCommand
from psqi.models import Questionnaire

class Command(BaseCommand):
    help = 'Modifica o valor em other_reasons_choice da tabela questionnaire'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='ID do registro a ser modificado')
        parser.add_argument('other_reasons_choice', type=str, help='Novo valor para other_reasons_choice')

    def handle(self, *args, **kwargs):
        record_id = kwargs['id']
        other_reasons_choice = kwargs['other_reasons_choice']

        try:
            questionnaire = Questionnaire.objects.get(id=record_id)
            questionnaire.other_reasons_choice = other_reasons_choice  # Atualiza o campo
            questionnaire.save()
            self.stdout.write(self.style.SUCCESS(f'Valor de other_reasons_choice atualizado para o registro ID {record_id}: "{other_reasons_choice}".'))
        except Questionnaire.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Registro com ID {record_id} não encontrado.'))
