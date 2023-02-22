from django.db import models
from django.contrib.postgres import fields


class Quiz(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  prompt = models.CharField(max_length=200)

  def __str__(self):
    return self.prompt


class Answer(models.Model):
  question = models.OneToOneField(Question, on_delete=models.CASCADE)
  correct_answer = models.CharField(max_length=200)

  class Meta:
    abstract = True




# class MultipleChoiceAnswer(Answer):
#   choices = fields.ArrayField(models.CharField(max_length=200, blank=True))

#   def __str__(self):
#     return f"{self.correct_answer} from {self.choices}"

#   def is_correct(self, user_answer):
#     return user_answer == self.correct_answer