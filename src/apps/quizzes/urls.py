from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<slug:quiz_slug>/', views.QuizView.as_view(), name='quiz'),
  path('<slug:quiz_slug>/grade/', views.grade, name='grade'),
  path('<slug:quiz_slug>/submit/', views.submit, name='submit'),
]