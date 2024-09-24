from django.shortcuts import get_object_or_404
from psqi.models import TestScore
import google.generativeai as genai


genai.configure(api_key='SUA_API')

def get_evaluation(questionnaire):
    test_score = get_object_or_404(TestScore, questionnaire=questionnaire)

    total_score = test_score.total_score
    sleep_quality = test_score.sleep_quality
    sleep_latency = test_score.sleep_latency
    sleep_duration = test_score.sleep_duration
    sleep_efficiency = test_score.sleep_efficiency
    sleep_disorders = test_score.sleep_disorders
    sleeping_pills = test_score.sleeping_pills
    daytime_dysfunction = test_score.daytime_dysfunction
    other_reasons = questionnaire.other_reasons


    generate = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
Gere uma avaliação do teste de PSQI do paciente com base nas notas abaixo, levando em conta as situações das notas específicas e o impacto na pontuação total {total_score}, SEM UTILIZAR ASTERISCOS OU OUTRAS FORMATAÇÕES E SÍMBOLOS.

As notas variam de 0 a 3, onde 0 indica nenhum problema e 3 indica problemas recorrentes.

Notas:
- Qualidade do sono: {sleep_quality}
- Latência do sono: {sleep_latency}
- Duração do sono: {sleep_duration}
- Eficiência do sono: {sleep_efficiency}
- Distúrbios do sono: {sleep_disorders}
- Uso de medicamentos para dormir: {sleeping_pills}
- Disfunção diurna: {daytime_dysfunction}

{f"Além disso, o paciente relatou os seguintes motivos adicionais para problemas de sono: {other_reasons}." if other_reasons else ""}

A pontuação total do paciente é {total_score}. Descreva cada nota individualmente, comentando sobre o impacto na qualidade do sono e na saúde do paciente. Faça um resumo geral com base na pontuação total e inclua recomendações. FAÇA DE FORMA SUCINTA!
"""
    
    response = generate.generate_content(prompt).text
    return response
