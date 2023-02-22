from django.contrib import admin

from .models import Quiz, Question, Choice, QuizForm, QuestionForm

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3


class QuestionInline(admin.TabularInline):
  model = Question
  extra = 5


class QuestionFormInline(admin.TabularInline):
  model = QuestionForm
  extra = 5


class QuizFormAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['quiz_name']}),
    ('Results', {'fields': ['quiz_completions',
                            'average_score'],
                 'classes': ['collapse']}),
    ('Date Information', {'fields': ['pub_date']}),
  ]
  inlines = [QuestionFormInline]
  list_display = ('quiz_name', 'quiz_completions', 'average_score', 'average_time')


class QuizAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['quiz_name']}),
    ('Results', {'fields': ['quiz_completions',
                            'average_score'],
                 'classes': ['collapse']}),
    ('Date Information', {'fields': ['pub_date']}),
  ]
  inlines = [QuestionInline]
  list_display = ('quiz_name', 'quiz_completions', 'average_score', 'average_time')

  
class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {"fields": ["question_text"]}),
  ]
  inlines = [ChoiceInline]
  list_display = ('question_text', 'question_completions', 'average_score')
  
admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizForm)
