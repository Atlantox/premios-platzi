import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=100, verbose_name='The question')
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text

    class Meta():
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def was_published_recently(self):
        return self.pub_date > timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='Target Question', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100, verbose_name='The choice')
    votes = models.PositiveIntegerField(verbose_name='Votes', default=0)

    def __str__(self):
        return f'{self.question}: {self.choice_text}'

    class Meta():
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
