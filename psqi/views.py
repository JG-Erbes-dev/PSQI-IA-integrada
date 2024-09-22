from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from psqi.forms import PSQIForm
from psqi.models import Questionnaire, TestScore
from psqi.charts import create_score_graph
from datetime import date


@method_decorator(login_required(login_url='login'), name='dispatch')
class TestListView(ListView):
    model = Questionnaire
    template_name = 'test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return Questionnaire.objects.filter(participant_id=self.request.user.id).order_by('evaluation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context['tests']:
            evaluation_dates = []
            scores = []

            for questionnaire in context['tests']:
                evaluation_date_str = questionnaire.evaluation_date
                if evaluation_date_str:
                    year, month, day = evaluation_date_str.split('-')
                    evaluation_date = date(int(year), int(month), int(day))
                    evaluation_dates.append((questionnaire, evaluation_date))
                    total_score = TestScore.objects.get(questionnaire=questionnaire).total_score
                    scores.append(total_score)

            context['evaluation_data'] = evaluation_dates

            evaluation_dates = [eval_date.strftime('%Y-%m-%d') for _, eval_date in evaluation_dates]
            context['graph_html'] = create_score_graph(evaluation_dates, scores)

        return context




@method_decorator(login_required(login_url='login'), name='dispatch')
class NewTestView(CreateView):
    model = Questionnaire
    form_class = PSQIForm
    template_name = 'new_test.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors) 
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('test_detail', kwargs={'pk': self.object.pk})
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class TestDetailView(DetailView):
    model = Questionnaire
    template_name = 'test_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = self.get_object()
        test_score = get_object_or_404(TestScore, questionnaire=questionnaire)

        
        evaluation_date_str = questionnaire.evaluation_date
        if evaluation_date_str:
            year, month, day = evaluation_date_str.split('-')
            evaluation_date = date(int(year), int(month), int(day))
            context['evaluation_date'] = evaluation_date

        if test_score.daytime_dysfunction == 0:
            context['daytime_dysfunction_text'] = "Nenhuma no último mês"
        elif test_score.daytime_dysfunction == 1:
            context['daytime_dysfunction_text'] = "Menos de um vez por semana"
        elif test_score.daytime_dysfunction == 2:
            context['daytime_dysfunction_text'] = "Uma ou duas vezes por semana"
        else:
            context['daytime_dysfunction_text'] = "Três ou mais vezes na semana"

        context['sleep_quality'] = test_score.sleep_quality
        context['sleep_latency'] = test_score.sleep_latency
        context['sleep_duration'] = test_score.sleep_duration
        context['sleep_efficiency'] = test_score.sleep_efficiency
        context['sleep_disorders'] = test_score.sleep_disorders
        context['sleeping_pills'] = test_score.sleeping_pills
        context['daytime_dysfunction'] = test_score.daytime_dysfunction
        context['total_score'] = test_score.total_score
        context['score_evaluation'] = test_score.score_evaluation

        return context