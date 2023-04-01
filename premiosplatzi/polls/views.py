from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>WATAGATAPITUSBERRY</h1> <h2> ¿WHAT?</h2>")
