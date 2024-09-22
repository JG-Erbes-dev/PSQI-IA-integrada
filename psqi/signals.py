from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from psqi.models import Questionnaire, TestScore
from gemini_api.client import get_evaluation


@receiver(post_save, sender=TestScore)
def set_score_evaluation(sender, instance, created, **kwargs):
    if created or not instance.score_evaluation:
        sleep_quality = instance.sleep_quality
        sleep_latency = instance.sleep_latency
        sleep_duration = instance.sleep_duration
        sleep_efficiency = instance.sleep_efficiency
        sleep_disorders = instance.sleep_disorders
        sleeping_pills = instance.sleeping_pills
        daytime_dysfunction = instance.daytime_dysfunction

        print("Valores para avaliação:", sleep_quality, sleep_latency, sleep_duration, sleep_efficiency, sleep_disorders, sleeping_pills, daytime_dysfunction)

        try:
            instance.score_evaluation = get_evaluation(instance.questionnaire)
            print("Avaliação definida:", instance.score_evaluation)

            instance.save(update_fields=['score_evaluation'])
        except Exception as e:
            print("Erro ao calcular avaliação:", e)


@receiver(post_save, sender=Questionnaire)
def create_or_update_testscore(sender, instance, created, **kwargs):
    test_score, created = TestScore.objects.get_or_create(questionnaire=instance)

    test_score.save()

    if created:
        print("Novo TestScore criado.")
    else:
        print("TestScore atualizado.")