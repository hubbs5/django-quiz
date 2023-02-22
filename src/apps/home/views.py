from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Quiz, Question, Choice


class IndexView(generic.ListView):
  template_name = "home/index.html"
  context_object_name = "quiz_list"

  def get_queryset(self):
    return Quiz.objects.filter(
      pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
  model = Question
  template_name = "home/detail.html"


class ResultsView(generic.DetailView):
  model = Question
  template_name = "home/results.html"

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
  