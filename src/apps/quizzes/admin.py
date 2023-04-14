from django.contrib import admin

from .models import Quiz, Question, Choice, Rubric


class QuestionInline(admin.TabularInline):
  model = Question
  extra = 4


class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3


class RubricInline(admin.TabularInline):
  model = Rubric
  extra = 3

class QuizAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['quiz_name',
                       'quiz_description',
                       'active',
                       'slug']}),
    ('Results', {'fields': ['quiz_attempts',
                            'average_score'],
                 'classes': ['collapse']})
  ]
  inlines = [QuestionInline,
             RubricInline]
  list_display = ('quiz_name', 'quiz_attempts', 'average_score')


class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['question_text']})
  ]
  inlines = [ChoiceInline]
  list_display = ('question_text', 'question_completions', 'average_score')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)