from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


DIFFICULTY_CHOICES = [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
]

QUALITY_CHOICES = [
    (0, 'Muito boa'),
    (1, 'Boa'),
    (2, 'Ruim'),
    (3, 'Muito ruim')
]

PARTNER_CHOICES = [
    (0, 'Não'),
    (1, 'Parceiro ou colega, mas em outro quarto'),
    (1, 'Parceiro no mesmo quarto, mas em outra cama'),
    (1, 'Parceiro na mesma cama')
]

DIFFICULTY_ENTHUSIASM = [
    (0, 'Nenhuma dificuldade'),
    (1, 'Problema leve'),
    (2, 'Problema razoável'),
    (3, 'Grande problema')
]

class Questionnaire(models.Model):
    evaluation_date = models.TextField(max_length=12, null=True)

    participant_name = models.CharField(max_length=250, verbose_name=_('NOME DO PARTICIPANTE (SOCIAL)'))
    participant_id = models.IntegerField(verbose_name=_('ID:'))
    birth_date = models.DateField(verbose_name=_('DATA DE NASCIMENTO'))

    bedtime = models.TimeField(max_length=250, verbose_name=_('1. Durante o último mês, quando você geralmente foi para a cama a noite?'))
    time_to_sleep = models.CharField(max_length=50, verbose_name=_('2. Durante o último mês, quanto tempo (em minutos) você geralmente levou para dormir a noite?'))
    wake_time = models.TimeField(max_length=250, verbose_name=_('3. Durante o último mês, quando você geralmente levantou de manhã?'))
    sleep_duration = models.CharField(max_length=50, verbose_name=_('4. Durante o último mês, quantas horas de sono você teve por noite? (Este pode ser diferente do número de horas que você ficou na cama)'))

    difficulty_falling_asleep = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('A) não conseguiu adormecer em até 30 minutos')
    )
    waking_up_night = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('B) acordou no meio da noite ou de manhã cedo')
    )
    bathroom_night = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('C) precisou levantar para ir ao banheiro')
    )
    difficulty_breathing = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('D) não conseguiu respirar confortavelmente')
    )
    coughing_snoring = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('E) tossiu ou roncou forte')
    )
    feeling_cold = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('F) sentiu muito frio')
    )
    feeling_hot = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('G) sentiu muito calor')
    )
    bad_dreams = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('H) teve sonhos ruins')
    )
    pain_at_night = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('I) teve dor')
    )
    other_reasons = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('J) outra(s) razão(ões), por favor descreva:'
                       'Com que frequência, durante o último mês, você teve dificuldade para dormir devido a essa razão?')
    )
    other_reasons_choice = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        blank=True,
        default=0,
        )
    sleep_quality = models.IntegerField(
        choices=QUALITY_CHOICES,
        verbose_name=_('6. Durante o último mês como você classificaria a qualidade do seu sono de uma maneira geral:')
    )
    sleep_medication_use = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('7. Durante o último mês, com que frequência você tomou medicamento (prescrito ou "por conta própria") para lhe ajudar a dormir?')
    )
    difficulty_staying_awake = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        verbose_name=_('8. No último mês, que frequência você teve dificuldade para ficar acordado enquanto dirigia, comia ou participava de uma atividade social (festa, reunião de amigos, trabalho, estudo)')
    )
    difficulty_enthusiasm = models.IntegerField(
        choices=DIFFICULTY_ENTHUSIASM,
        verbose_name=_('9. Durante o último mês, quão problemático foi pra você manter o entusiasmo (ânimo) para fazer as coisas (suas atividades habituais)?')
    )
    partner_presence = models.IntegerField(
        choices=PARTNER_CHOICES,
        verbose_name=_('10. Você tem um(a) parceiro [esposo(a)] ou colega de quarto?')
    )

    class Meta:
        verbose_name = _('Questionário PSQI')
        verbose_name_plural = _('Questionários PSQI')
        
    def __str__(self):
        return f"Questionário PSQI de {self.participant_name} - Avaliado em {self.evaluation_date}"
        

class TestScore(models.Model):
    questionnaire = models.OneToOneField(Questionnaire, on_delete=models.CASCADE, related_name='psqi_score')

    sleep_quality = models.IntegerField(default=0)
    sleep_latency = models.IntegerField(default=0)
    sleep_duration = models.FloatField(default=0)
    sleep_efficiency = models.IntegerField(default=0)
    sleep_disorders = models.IntegerField(default=0)
    sleeping_pills = models.IntegerField(default=0)
    daytime_dysfunction = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    score_evaluation = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not hasattr(self, '_sleep_duration_calculated'):
            self._sleep_duration_calculated = True 

            self.sleep_quality = self.sleep_quality_calc()
            self.sleep_latency = self.sleep_latency_calc()
            
            if self.sleep_duration is None:
                self.sleep_duration = self.sleep_duration_calc()
            
            self.sleep_efficiency = self.sleep_efficiency_calc()
            self.sleep_disorders = self.sleep_disorders_calc()
            self.daytime_dysfunction = self.daytime_dysfunction_calc()

        print("Valores antes de calcular o total_score:", 
            self.sleep_quality, self.sleep_latency, 
            self.sleep_duration, self.sleep_efficiency, 
            self.sleep_disorders, self.daytime_dysfunction)

        self.total_score = self.score_calc()
        print("Total Score calculado:", self.total_score)

        super().save(*args, **kwargs)

    def score_calc(self):
        return (
            self.sleep_quality +
            self.sleep_latency +
            self.sleep_duration +
            self.sleep_efficiency +
            self.sleep_disorders +
            self.sleeping_pills +
            self.daytime_dysfunction
        )

    def sleep_quality_calc(self):
        return self.sleep_quality

    def sleep_latency_calc(self):
        time_to_sleep_str = self.questionnaire.time_to_sleep
        try:
            time_to_sleep = int(float(time_to_sleep_str))
        except ValueError:
            time_to_sleep = 0

        if time_to_sleep <= 15:
            time_to_sleep = 0
        elif 16 <= time_to_sleep <= 30:
            time_to_sleep = 1
        elif 31 <= time_to_sleep <= 60:
            time_to_sleep = 2
        else:
            time_to_sleep = 3

        difficulty_falling_asleep = self.questionnaire.difficulty_falling_asleep
        sleep_latency = time_to_sleep + difficulty_falling_asleep

        return sleep_latency

    def sleep_duration_calc(self):
        sleep_duration = float(self.sleep_duration)
        print(f"Duração do sono (depois do cálculo): {sleep_duration}")

        if sleep_duration >= 7:
            return 0
        elif 6 <= sleep_duration < 7:
            return 1
        elif 5 <= sleep_duration < 6:
            return 2
        else:
            return 3


    def sleep_efficiency_calc(self):
        try:
            bedtime = datetime.combine(datetime.today(), self.questionnaire.bedtime)
            wake_time = datetime.combine(datetime.today(), self.questionnaire.wake_time)
            
            total_bedtime_hours = (wake_time - bedtime).total_seconds() / 3600
            if total_bedtime_hours <= 0:
                return 0 
            efficiency = (float(self.sleep_duration) / total_bedtime_hours) * 100
            if efficiency > 85:
                return 0
            elif 75 <= efficiency <= 84:
                return 1
            elif 65 <= efficiency <= 74:
                return 2
            else:
                return 3
        except (ValueError, ZeroDivisionError):
            return 3

    def sleep_disorders_calc(self):
        sleep_disorders_total = (
            self.questionnaire.waking_up_night +
            self.questionnaire.bathroom_night +
            self.questionnaire.difficulty_breathing +
            self.questionnaire.coughing_snoring +
            self.questionnaire.feeling_cold +
            self.questionnaire.feeling_hot +
            self.questionnaire.bad_dreams + 
            self.questionnaire.pain_at_night +
            self.questionnaire.other_reasons_choice
        )

        if sleep_disorders_total >= 19:
            return 3
        elif 10 <= sleep_disorders_total <= 18:
            return 2
        elif 1 <= sleep_disorders_total <= 9:
            return 1
        else:
            return 0

    def daytime_dysfunction_calc(self):
        daytime_dysfunction = (
            self.questionnaire.difficulty_staying_awake +
            self.questionnaire.difficulty_enthusiasm
        )

        if daytime_dysfunction >= 5:
            return 3
        elif 3 <= daytime_dysfunction <= 4:
            return 2
        elif 1 <= daytime_dysfunction <= 2:
            return 1
        else:
            return 0

    def __str__(self):
        return (f"Pontuação total do PSQI para {self.questionnaire.participant_name} "
                f"- Avaliado em {self.questionnaire.evaluation_date}: {self.total_score}")
