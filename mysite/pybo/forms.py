from django import forms
from django.forms import widgets
from pybo.models import Finance, Question ,Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  
        label = {
            'subject':'제목',
            'content':'내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content':'답변내용',
        }

class FinanceForm(forms.ModelForm):
    class Meta:
        model = Finance
        fields = ['Date','Open','Close']
        labels = {
            'Date':'날짜',
            'Open':'시가',
            'Close':'종가'
        }
