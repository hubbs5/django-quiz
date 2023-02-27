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


def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  context = {'question': question}
  return render(request, 'quizzes/results.html', context=context)


def grade(request, question_id):
  # quiz = get_object_or_404(Quiz, pk=quiz_id)
  question = get_object_or_404(Question, pk=question_id)
  num_questions = 1
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    context = {'question': question,
               'error_message': "You didn't make a selection."}
    return render(request, 'quizzes/results.html', context=context)
  else:
    selected_choice.selections += 1
    selected_choice.save()
    points = 1 if selected_choice.correct else 0
    score = f'{points / num_questions * 100:.1f}%' # Only checks one question at a time
    context = {
      'question': question,
      'choice': selected_choice,
      'points': points,
      'score': score,
    }
    return render(request, 'quizzes/results.html', context=context)


def grade_quiz(request, quiz_id):
  quiz = get_object_or_404(Quiz, pk=quiz_id)
  if request.method == 'POST':
    questions = quiz.question_set.all()
    points = 0
    for i, q in enumerate(questions):
      # TODO: get individual choices if choice.correct = True then +1 to points
      pass

    score = points / (i + 1)

    context = {
      'quiz': quiz,
      'points': points,
      'score': score
    }

    return render(request, 'quizzes/results.html', context=context)
