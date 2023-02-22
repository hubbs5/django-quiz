from django.db import models
from django.utils import timezone

from datetime import timedelta

class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  search_fields = ['question_text']
  class Meta:
    app_label = "home"

  def __str__(self) -> str:
    return self.question_text

  def was_published_recently(self):
    return self.pub_date >= timezone.now() - timedelta(days=1)


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)
  
  def __str__(self) -> str:
    return self.choice_text