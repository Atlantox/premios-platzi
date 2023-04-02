from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),  # ex: polls/
    path('<int:pk>/', views.DetailView.as_view(), name='details'),  # ex: polls/5
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),  # ex: polls/2/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),  # ex: polls/3/vote
]