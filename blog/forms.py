from django import forms
from django.contrib.auth.forms import UserCreationForm
from blog.models import Question, Profile, Answer
from django.contrib.auth.models import User
from pprint import pformat
from django.forms import Textarea
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
			self._errors["username"] = self.error_class([u""])
			self._errors["password"] = self.error_class([u""])
			del self.cleaned_data["username"]
			del self.cleaned_data["password"]
			raise forms.ValidationError("Sorry, that username or password was invalid. Please, try again.")
		return self.cleaned_data

class AskForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']

		widgets = {
            'tags': CheckboxSelectMultiple(),
        }

class RegisterForm(UserCreationForm):
	nickname = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'nickname', 'password1', 'password2']

	def clean(self):
		user = User.objects.filter(username=self.cleaned_data.get('username'))
		if user:
			msg = u"This username has already been taken!"
			self._errors["username"] = self.error_class([msg])
			del self.cleaned_data["username"]
		profile = Profile.objects.filter(email=self.cleaned_data.get('email'))
		if profile:
			msg = u"This email has already been taken!"
			self._errors["email"] = self.error_class([msg])
			del self.cleaned_data["email"]
		
		return self.cleaned_data


class SettingsForm(forms.ModelForm):
	username = forms.CharField(required=True)

	class Meta:
		model = Profile
		fields = ['username', 'email', 'nickname', 'avatar']

	def clean(self):
		user = User.objects.filter(username=self.cleaned_data.get('username'))
		if user:
			msg = u"This username has already been taken!"
			self._errors["username"] = self.error_class([msg])
			del self.cleaned_data["username"]
		profile = Profile.objects.filter(email=self.cleaned_data.get('email'))
		if profile:
			msg = u"This email has already been taken!"
			self._errors["email"] = self.error_class([msg])
			del self.cleaned_data["email"]
		
		return self.cleaned_data
		
class AnswerForm(forms.ModelForm):

	class Meta:
		model = Answer
		fields = ['text']

		widgets = {
            'text': Textarea(attrs={'cols': 60,'rows': 8}),
        }

