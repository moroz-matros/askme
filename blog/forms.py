from django import forms
from django.contrib.auth.forms import UserCreationForm
from blog.models import Question, Profile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

class AskForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']

class RegisterForm(UserCreationForm):
	nickname = forms.CharField(required=True)

	class Meta:
		
		model = User
		fields = ['username', 'email', 'nickname', 'password1', 'password2']