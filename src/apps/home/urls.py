from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
  path("", views.IndexView.as_view(), name="home"),
  path("<int:quiz_id>/question/", views.simple_question_form, name='simple_question'),
  # path("<int:pk>/", views.QuizView.as_view(), name="quiz"),
  path("<int:quiz_id>/", views.quiz, name='quiz'),
  path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
  path("<int:pk>/quiz-results/", views.QuizResultsView.as_view(), name='quiz_results'),
  path("<int:question_id>/grade/", views.grade, name='grade'),
  path("<int:question_id>/vote/", views.vote, name="vote"),
]