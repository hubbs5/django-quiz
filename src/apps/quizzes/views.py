from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Quiz, Question, Choice


class IndexView(generic.ListView):
  template_name = 'quizzes/index.html'
  context_object_name = 'quiz_list'

  def get_queryset(self):
    return Quiz.objects.all()

class QuizView(generic.DetailView):
  model = Quiz
  template_name = 'quizzes/quiz.html'


class DetailView(generic.DetailView):
  model = Quiz
  template_name = 'quizzes/detail.html'


class ResultsView(generic.DetailView):
  model = Quiz
  template_name = 'quizzes/results.html'


def grade(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    context = {'question': question,
               'error_message': "You didn't make a selection."}
    return render(request, 'quizzes/detail.html', context=context)
  else:
    selected_choice.selections += 1
    selected_choice.save()
    return HttpResponseRedirect(
      reverse('quizzes:results', args=(question.id,)))
