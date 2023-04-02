from django.contrib import admin
from . import models

class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    search_fields = ['question_text']
    list_display = ['id', 'question_text', 'pub_date', 'was_published_recently']
    list_filter = ['pub_date']
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ['votes']

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Choice, ChoiceAdmin)
