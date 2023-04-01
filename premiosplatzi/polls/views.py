from django.shortcuts import render
from django.http import HttpResponse

from . import models


def index(request):
    questions = models.Question.objects.all()

    ctx = { 'latest_question_list':questions }
    
    return render(request, 'polls/index.html', ctx)


def details(request, question_id):
    return HttpResponse(f'Estás viendo la question {question_id}')


def results(request, question_id):
    return HttpResponse(f'Estás viendo los resultados a la pregunta {question_id}')


def vote(request, question_id):
    return HttpResponse(f'Estás votando a la pregunta {question_id}')