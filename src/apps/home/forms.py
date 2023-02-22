from django import forms
from .models import SimpleQuestion

class SimpleQuestionForm(forms.ModelForm):
  class Meta:
    model = SimpleQuestion
    fields = '__all__'