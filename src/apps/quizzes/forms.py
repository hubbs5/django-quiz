from django import forms

class QuizSubmissionForm(forms.Form):
  email = forms.EmailField(required=True)
  first_name = forms.CharField(required=True)
  last_name = forms.CharField(required=True)