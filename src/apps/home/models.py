from django.db import models
from django import forms 
from django.utils import timezone

from datetime import timedelta


class Quiz(models.Model):
  quiz_name = models.CharField(max_length=200)
  pub_date = models.DateField('Date quiz was published.')
  search_fields = ['quiz_name']
  quiz_attempts = models.IntegerField(
    'Number of times quiz was attempted including incomplete attempts.',
    default=0)
  quiz_completions = models.IntegerField(
    'Number of times quiz was completed. Completion requires submission ' + \
    'of e-mail address.',
    default=0)
  average_score = models.FloatField(
    'Average score across all attempts.',
    default=0)
  average_score_completion = models.FloatField(
    'Average score for quiz.',
    default=0)
  average_time = models.FloatField(
    'Average time spent on quiz across all attempts.',
    default=0)
  average_time_to_completion = models.FloatField(
    'Average time to completion.',                                             
    default=0)
  class Meta:
    app_label = 'home'

  def __str__(self) -> str:
    return self.quiz_name
  

class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  question_text = models.CharField(max_length=200)
  question_completions = models.IntegerField(
    'number of times question was answered',
    default=0)
  average_score = models.FloatField(
    'average score for question',                                
    default=0)
  search_fields = ['question_text']
  answer = models.CharField(max_length=200)
  class Meta:
    app_label = 'home'

  def __str__(self) -> str:
    return self.question_text


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  selections = models.IntegerField(default=0)

  class Meta:
    app_label = 'home'
  
  def __str__(self) -> str:
    return self.choice_text

class QuizForm(models.Model):
  quiz_name = models.CharField(max_length=200)
  pub_date = models.DateField('Date quiz was published.')
  search_fields = ['quiz_name']
  quiz_attempts = models.IntegerField(
    'Number of times quiz was attempted including incomplete attempts.',
    default=0)
  quiz_completions = models.IntegerField(
    'Number of times quiz was completed. Completion requires submission ' + \
    'of e-mail address.',
    default=0)
  average_score = models.FloatField(
    'Average score across all attempts.',
    default=0)
  average_score_completion = models.FloatField(
    'Average score for quiz.',
    default=0)
  average_time = models.FloatField(
    'Average time spent on quiz across all attempts.',
    default=0)
  average_time_to_completion = models.FloatField(
    'Average time to completion.',                                             
    default=0)
  class Meta:
    app_label = 'home'

  def __str__(self) -> str:
    return self.quiz_name

class Question2(models.Model):
  quiz = models.ForeignKey(QuizForm, on_delete=models.CASCADE)
  question_text = models.CharField(max_length=200)
  question_completions = models.IntegerField(
    'number of times question was answered',
    default=0)
  average_score = models.FloatField(
    'average score for question',                                
    default=0)
  search_fields = ['question_text']
  answer = models.CharField(max_length=200)
  class Meta:
    app_label = 'home'

  def __str__(self) -> str:
    return self.question_text


class Choice2(models.Model):
  question = models.ForeignKey(Question2, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  selections = models.IntegerField(default=0)

  class Meta:
    app_label = 'home'
  
  def __str__(self) -> str:
    return self.choice_text

class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question2
    fields = '__all__'
    app_name = 'home'

class ChoiceForm(forms.ModelForm):
  class Meta:
    model = Choice2
    fields = '__all__'


class SimpleQuestion(models.Model):
  title = models.CharField(max_length=200)
  question_text = models.CharField(max_length=200)
  answers = models.ManyToManyField(Choice)

  def __str__(self) -> str:
    return self.question_text


class SimpleChoice(models.Model):
  simple_question = models.ForeignKey(SimpleQuestion,
                                      on_delete=models.CASCADE)