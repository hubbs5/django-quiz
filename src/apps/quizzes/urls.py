from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.QuizView.as_view(), name='quiz'),
  # path('<int:question_id>/', views.DetailView.as_view(), name='detail'),
  path('<int:question_id>/results/', views.results, name='results'),
  path('<int:question_id>/grade/', views.grade, name='grade'),
]