from django.db import models

class Quiz(models.Model):
  quiz_name = models.CharField(max_length=200)
  quiz_attempts = models.IntegerField(default=0)
  average_score = models.FloatField(default=0)

  class Meta:
    app_label = 'quizzes'

  def __str__(self) -> str:
    return self.quiz_name


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  question_text = models.CharField(max_length=200)
  question_completions = models.IntegerField(default=0)
  average_score = models.FloatField(default=0)

  class Meta:
    app_label = 'quizzes'

  def __str__(self) -> str:
    return self.question_text


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  selections = models.IntegerField(default=0)
  correct = models.BooleanField(default=False)

  class Meta:
    app_label = 'quizzes'

  def __str__(self) -> str:
    return self.choice_text
