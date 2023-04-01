from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),  # ex: polls/
    path('<int:question_id>/', views.details, name='Question_details'),  # ex: polls/5
    path('<int:question_id>/results/', views.results, name='Question_results'),  # ex: polls/2/results/
    path('<int:question_id>/vote/', views.vote, name='Question_vote'),  # ex: polls/3/vote
]