from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Quiz, Question, Choice, Rubric
from .forms import QuizSubmissionForm

from . import emails
class IndexView(generic.ListView):
  template_name = 'quizzes/index.html'
  context_object_name = 'quiz_list'

  def get_queryset(self):
    return Quiz.objects.filter(active=True)


class QuizView(generic.DetailView):
  model = Quiz
  template_name = 'quizzes/quiz.html'
  slug_field = 'slug'
  slug_url_kwarg = 'quiz_slug'


def grade(request, quiz_slug):
  # Grades the quiz, stores results in context, and redirects to the 
  # submission page.
  quiz = get_object_or_404(Quiz, slug=quiz_slug)
  form = QuizSubmissionForm(request.POST)
  context = {'quiz': quiz,
             'form': form}
  if request.method == 'POST':
    questions = quiz.question_set.all()
    score, unanswered = 0, 0
    for q in questions:
      try:
        pk = request.POST[f'question-{q.id}']
        selected_choice = q.choice_set.get(pk=pk)
        score += selected_choice.points
        selected_choice.selections += 1
        selected_choice.save()
        q.question_completions += 1
        q.average_score = q.average_score + (selected_choice.points - q.average_score) / q.question_completions
        q.save()
      except KeyError:
        unanswered += 1

    quiz.quiz_attempts += 1
    quiz.average_score = quiz.average_score + (score - quiz.average_score) / quiz.quiz_attempts
    quiz.save()

    rubric = _apply_rubric(quiz, score)
    context.update(rubric)
    context['score'] = score
    return render(request, 'quizzes/submit.html', context)

  return render(request, 'quizzes/quiz.html', context)


def submit(request, quiz_slug):
  context = {}
  if request.method == 'POST':
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    form = QuizSubmissionForm(request.POST)
    context['quiz'] = quiz
    if form.is_valid():
      emails.add_user_to_mailchimp(request.POST)
      emails.send_results_email(request.POST)
      return render(request, 'quizzes/success.html', context)

  context['form'] = QuizSubmissionForm(request.POST)
  return render(request, 'quizzes/submit.html', context)


def _apply_rubric(quiz, score):
  # Returns a dictionary of the rubric tag and description for the given
  # quiz and points.
  rubric = quiz.rubric_set.filter(quiz=quiz).order_by('-minimum_score')
  for r in rubric:
    if score >= r.minimum_score:
      r.count += 1
      r.save()
      return {'tag': r.tag,
              'display_description': r.display_description}
  # Return defaults
  return {'tag': quiz.quiz_name,
          'display_description': 'Thanks for taking the quiz!'}