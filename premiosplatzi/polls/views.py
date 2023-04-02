from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from . import models

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        ''' Returns the last five questions ordered by publish date '''
        return models.Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = models.Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        ''' Only return the questions in the past '''
        return models.Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    model = models.Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        ''' Only return the questions in the past '''
        return models.Question.objects.filter(pub_date__lte=timezone.now())
    


def vote(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    voted = False
    
    if question.pub_date > timezone.now():
        return HttpResponseNotFound('Poll not found')
    
    if request.POST['choice']:
        choices = question.choice_set.filter(pk=request.POST['choice'])
        if len(choices) == 1:
            choice = choices.first()
            choice.votes += 1
            choice.save()
            voted = True

    if voted:
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    else:
        return render(request, 'polls/details.html', {
            'question':question,
            'error_message': 'Has escogido una opción inválida'
        })
    