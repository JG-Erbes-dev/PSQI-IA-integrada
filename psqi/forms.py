from django import forms
from psqi.models import Questionnaire
from datetime import datetime, timedelta
import re
from psqi.models import DIFFICULTY_CHOICES, QUALITY_CHOICES, DIFFICULTY_ENTHUSIASM, PARTNER_CHOICES


class PSQIForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['evaluation_date', 'participant_name', 'participant_id', 'birth_date',
            'bedtime', 'time_to_sleep', 'wake_time', 'sleep_duration',
            'difficulty_falling_asleep', 'waking_up_night', 'bathroom_night',
            'difficulty_breathing', 'coughing_snoring', 'feeling_cold',
            'feeling_hot', 'bad_dreams', 'pain_at_night', 'other_reasons',
            'other_reasons_choice', 'sleep_quality', 'sleep_medication_use',
            'difficulty_staying_awake', 'difficulty_enthusiasm', 'partner_presence'
        ]
        widgets = {
            'evaluation_date': forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY', 'id': 'date'}),
            'participant_name': forms.TextInput(attrs={'placeholder': 'Nome do participante'}),
            'participant_id': forms.NumberInput(attrs={'placeholder': 'ID do participante'}),
            'birth_date': forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY', 'id': 'birthdate'}),
            'bedtime': forms.TimeInput(attrs={'type': 'time'}),
            'time_to_sleep': forms.NumberInput(attrs={'placeholder': 'Ex: 30 (minutos)'}),
            'wake_time': forms.TimeInput(attrs={'type': 'time'}),
            'sleep_duration': forms.NumberInput(attrs={'placeholder': 'Ex: 7 (horas)'}),
            'difficulty_falling_asleep': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'waking_up_night': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'bathroom_night': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'difficulty_breathing': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'coughing_snoring': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'feeling_cold': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'feeling_hot': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'bad_dreams': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'pain_at_night': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'other_reasons': forms.TextInput(attrs={
                'style': 'display:inline; border-bottom: 1px solid; border-color: #000000; '
                        'border-top: none; border-left: none; border-right: none; '
                        'background: none; width: 90px;',
            }),
            'other_reasons_choice': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'sleep_quality': forms.RadioSelect(choices=QUALITY_CHOICES),
            'sleep_medication_use': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'difficulty_staying_awake': forms.RadioSelect(choices=DIFFICULTY_CHOICES),
            'difficulty_enthusiasm': forms.RadioSelect(choices=DIFFICULTY_ENTHUSIASM),
            'partner_presence': forms.RadioSelect(choices=PARTNER_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['participant_name'].widget.attrs['value'] = user.get_full_name()
            self.fields['participant_id'].widget.attrs['value'] = user.id
            self.fields['birth_date'].widget.attrs['value'] = user.date_of_birth.strftime("%d/%m/%Y")

    def clean_evaluation_date(self):
        evaluation_date = self.cleaned_data.get('evaluation_date')

        if evaluation_date:
            if isinstance(evaluation_date, str):
                try:
                    return datetime.strptime(evaluation_date, "%d/%m/%Y").date()
                except ValueError:
                    raise forms.ValidationError('Formato de data inválido. Use o formato DD/MM/YYYY.')
            return evaluation_date
        
        raise forms.ValidationError('Este campo é obrigatório.')
    
    def clean_time_to_sleep(self):
        time_to_sleep = self.cleaned_data.get('time_to_sleep')
        
        if time_to_sleep is not None:
            match = re.search(r'(\d+)', str(time_to_sleep))
            if match:
                time_to_sleep = float(match.group(1))  
                
                if time_to_sleep < 0:
                    raise forms.ValidationError('O tempo para dormir não pode ser negativo.')
            else:
                raise forms.ValidationError('Insira um valor numérico válido para o tempo para dormir.')
        
        return time_to_sleep

    def clean_sleep_duration(self):
        sleep_duration = self.cleaned_data.get('sleep_duration')

        if sleep_duration:
            sleep_duration = sleep_duration.strip().lower()
            hours = 0

            match = re.match(r'(\d+)\s*horas?', sleep_duration)
            if match:
                hours = float(match.group(1))

            if 'e meia' in sleep_duration:
                hours += 0.5

            match = re.search(r'(\d+)\s*minutos?', sleep_duration)
            if match:
                minutes = float(match.group(1)) / 60
                hours += minutes

            return hours

        raise forms.ValidationError('Este campo é obrigatório.')

    def clean(self):
        cleaned_data = super().clean()

        required_fields_part1 = [
            'evaluation_date', 
            'participant_name', 
            'participant_id', 
            'birth_date', 
            'bedtime', 
            'time_to_sleep', 
            'wake_time', 
            'sleep_duration'
        ]

        for field in required_fields_part1:
            if not cleaned_data.get(field):
                raise forms.ValidationError('Por favor, preencha todos os campos da primeira parte do formulário.')

        required_fields_part2 = [
            'difficulty_falling_asleep', 
            'waking_up_night', 
            'bathroom_night', 
            'difficulty_breathing', 
            'coughing_snoring', 
            'feeling_cold', 
            'feeling_hot', 
            'bad_dreams', 
            'pain_at_night', 
            'sleep_quality', 
            'sleep_medication_use', 
            'difficulty_staying_awake', 
            'difficulty_enthusiasm', 
            'partner_presence'
        ]

        for field in required_fields_part2:
            if cleaned_data.get(field) is None:
                print(field.errors)
                raise forms.ValidationError('Por favor, preencha todos os campos da segunda parte do formulário.')

        bedtime = cleaned_data.get('bedtime')
        wake_time = cleaned_data.get('wake_time')
        sleep_duration = cleaned_data.get('sleep_duration') 

        if bedtime and wake_time and sleep_duration is not None:
            sleep_duration_delta = timedelta(hours=sleep_duration)

            expected_wake_time = (datetime.combine(datetime.today(), bedtime) + sleep_duration_delta).time()

            if wake_time < expected_wake_time:
                self.add_error('wake_time', 'A hora de acordar deve ser igual ou maior que a hora de deitar somada à duração do sono.')

        return cleaned_data
