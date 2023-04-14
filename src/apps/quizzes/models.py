from django.db import models
from django.utils.text import slugify

class Quiz(models.Model):
  quiz_name = models.CharField(max_length=200)
  slug = models.SlugField(max_length=100, blank=True) #, unique=True) #add this once slugs have been created
  quiz_description = models.CharField(max_length=500,
                                      default="None")
  quiz_attempts = models.IntegerField(default=0)
  average_score = models.FloatField(default=0)
  active = models.BooleanField(default=False)

  class Meta:
    app_label = 'quizzes'

  def __str__(self) -> str:
    return self.quiz_name

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.quiz_name)
    super().save(*args, **kwargs)


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
  points = models.IntegerField(default=0)

  class Meta:
    app_label = 'quizzes'

  def __str__(self) -> str:
    return self.choice_text


class Rubric(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  display_description = models.CharField(max_length=200)
  minimum_score = models.FloatField(default=0)
  tag = models.CharField(max_length=200, default="")
  count = models.IntegerField(default=0)

  class Meta:
    app_label = 'quizzes'

  def __str__(self) -> str:
    return f"{self.minimum_score} is required for {self.tag}"