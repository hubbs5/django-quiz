from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<int:quiz_id>/', views.QuizView.as_view(), name='quiz'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
  path('<int:question_id>/grade/', views.grade, name='grade'),
]