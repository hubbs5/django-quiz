from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Quiz, Question, Choice, SimpleQuestion
from .forms import SimpleQuestionForm, QuestionForm


def simple_question_form(request, quiz_id):
  quiz = get_object_or_404(Quiz, pk=quiz_id)
  context = {
    'quiz': quiz
  }
  if request.method == "POST":
    questions = quiz.question_set.all()
    points = 0
    for i, q in enumerate(questions):
      print(x)
      print(f"Question = {request.POST.get(q.question)}")
      if request.POST.get(q.question) == q.answer:
        points += 1

    score = points / i * 100
    context = {
      'quiz': quiz,
      'points': points,
      'score': score,
    }
    return render(
      request,
      template_name='home/quiz_results.html',
      context=context
    )
  return render(request,
                template_name='home/quiz_forms.html', 
                context=context)


def _simple_question_form(request):
  if request.method == "POST":
    question_form = SimpleQuestionForm(request.POST)
    if question_form.is_valid():
      question_form.save()
      messages.success(request, ('Submission successfully added!'))
    else:
      messages.error(request, 'Error submitting values.')

    return redirect('/')

  question_form = SimpleQuestionForm()
  questions = SimpleQuestion.objects.all()
  context = {
    'question_form': question_form,
    'questions': questions,
  }
  return render(
    request,
    template_name='home/simple_question_form.html',
    context=context)
      

class IndexView(generic.ListView):
  template_name = "home/index.html"
  context_object_name = "quiz_list"

  def get_queryset(self):
    return Quiz.objects.filter(
      pub_date__lte=timezone.now()).order_by("-pub_date")


class QuizView(generic.DetailView):
  # Note: This generally works, but I'm not sure how to get the
  # quiz scored or submitted at this point
  model = Quiz
  template_name = 'home/quiz.html'

class DetailView(generic.DetailView):
  model = Question
  template_name = "home/detail.html"


class ResultsView(generic.DetailView):
  model = Question
  template_name = "home/quiz_results.html"


class QuizResultsView(generic.DeleteView):
  model = Question
  template_name = 'home/quiz_results.html'


# def quiz(request, quiz_id):
#   quiz = get_object_or_404(Quiz, pk=quiz_id)
#   context = {'quiz': quiz}
#   return render(request, template_name='home/quiz.html', context=context)


def quiz(request, quiz_id):
  quiz = get_object_or_404(Quiz, pk=quiz_id)
  if request.method == "POST":
    print(request.POST)
    questions = quiz.question_set.all()
    points = 0
    for i, q in enumerate(questions):
      print(f"Question = {request.POST.get(q.question)}")
      if request.POST.get(q.question) == q.answer:
        points += 1

    score = points / i * 100
    context = {
      'points': points,
      'score': score,
      'quiz': quiz,
    }
    if request.user.is_authenticated:
      return render(request, 'home/results.html', context)
    else:
      return render(request, 'home/enter-email.html', context)
  else:
    context = {'quiz': quiz}
    return render(request, 'home/quiz.html', context)


def contact_form(request, context):
  pass


def home(request):
  latest_question_list = Question.objects.order_by('-pub_date')
  context = {"latest_question_list": latest_question_list}
  return render(request, template_name="home/index.html", context=context)


def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  context = {"question": question}
  return render(request, template_name="home/detail.html", context=context)


def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  context = {"question": question}
  return render(request, 'home/results.html', context)


def grade(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    context = {'question': question,
               'error_message': "You didn't make a selection."}
    return render(request, 'home/detail.html', context=context)
  else:
    selected_choice.selections += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('home:results', args=(question.id,)))
      


def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST["choice"])
  except (KeyError, Choice.DoesNotExist):
    context = {"question": question,
               "error_message": "You didn't select a choice."}
    return render(request, 'home/detail.html', context=context)
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('home:results', args=(question.id,)))
  