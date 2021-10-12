from django.contrib import admin
from .models import Question , Finance



class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

class FinanceAdmin(admin.ModelAdmin):
    search_fields = ['Open']

admin.site.register(Finance,FinanceAdmin)
admin.site.register(Question,QuestionAdmin)
# Register your models here.
