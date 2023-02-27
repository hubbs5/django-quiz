from django import forms
from .models import SimpleQuestion, Question


class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = '__all__'

class SimpleQuestionForm(forms.ModelForm):
  class Meta:
    model = SimpleQuestion
    fields = '__all__'