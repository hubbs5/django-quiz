from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import *

class IndexView(generic.ListView):
    model = Quiz
    template_name = "quizzes/index.html"

def display_quiz(request, quiz_id):
  quiz = get_object_or_404(Quiz, pk=quiz_id)
  question = quiz.question_set.first()
  return redirect(reverse("quizzes:display_question", 
                          kwargs={
                            "quiz_id": quiz_id,
                            "question_id": question.pk
                            }))


def display_question(request, quiz_id, question_id):
  quiz = get_object_or_404(Quiz, pk=quiz_id)
  questions = quiz.question_set.all()
  current_question, next_question = None, None
  for i, question in enumerate(questions):
    if question.pk == question_id:
      current_question = question
      if i != len(questions) - 1:
        next_question = questions[i + 1]

  return render(
    request,
    "quiz/display.html",
    {"quiz": quiz,
     "question": current_question,
     "next_question": next_question},
  )


def grade_question(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  answer = getattr(question, "multiplechoiceanswer", None) or \
    getattr(question, "freetextanswer")
  is_correct = answer.is_correct(request.POST.get("answer"))
  return render(
    request,
    "quiz/partial.html",
    {"is_correct": is_correct,
     "correct_answer": answer.correct_answer},
  )


def add_question(request):
  if request.user.is_staff:
    form = addQuestionForm()
    if request.method == "POST":
      form = addQuestionForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect("/")
    context = {"form": form}
    return render(request, "quizzes/add-question.html", context)
  else:
    return redirect("index")


def results_page(request):
  if request.user.is_authenticated:
    # TODO: add function to email results
    return redirect("index")
  else:
    form = addContactInfoForm()
    if request.method == "POST":
      form = addContactInfoForm(request.POST)
      if form.is_valid():
        # TODO: add function to email results
        form.save()
        return redirect("index")
    context = {
      "form": form
    }
    return render(request, "quizzes/success.html", context)