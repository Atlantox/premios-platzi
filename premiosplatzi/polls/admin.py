from django.contrib import admin
from . import models

class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ['votes']

admin.site.register(models.Question)
admin.site.register(models.Choice, ChoiceAdmin)
