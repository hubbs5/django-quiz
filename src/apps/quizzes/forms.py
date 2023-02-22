from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username','password'] 


class addQuestionForm(ModelForm):
  class Meta:
    model = Question
    fields = "__all__"


class addContactInfoForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["email", "first_name"]