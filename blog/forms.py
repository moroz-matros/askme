from django import forms
from django.contrib.auth.forms import UserCreationForm
from blog.models import Question, Profile, Answer
from django.contrib.auth.models import User
from pprint import pformat
from django.forms import Textarea
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
from django.contrib.auth import authenticate

from crispy_forms.helper import FormHelper

from pprint import pformat

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

	def __init__(self, *args, **kwargs):
		self.profile = kwargs.pop('profile',None)
		print(self.profile)
		super(AskForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		question = super().save(commit=False)
		question.author = self.profile
		question.save()
		self.save_m2m()
		return question

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

	def save(self, *args, **kwargs):
		user = super().save(*args, **kwargs)
		user.refresh_from_db()  # load the profile instance created by the signal
		user.profile.nickname = self.cleaned_data.get('nickname')
		user.profile.email = self.cleaned_data.get('email')
		user.profile.save()
		return user



class SettingsForm(forms.ModelForm):
	username = forms.CharField(required=True)

	class Meta:
		model = Profile
		fields = ['username', 'email', 'nickname', 'avatar']

	def clean(self):
		user = User.objects.filter(username=self.cleaned_data.get('username'))
		if user and (user.get().id != self.user.id):
			msg = u"This username has already been taken!"
			self._errors["username"] = self.error_class([msg])
			del self.cleaned_data["username"]
		profile = Profile.objects.filter(email=self.cleaned_data.get('email'))
		if profile and (profile.get().id != self.user.profile.id):
			msg = u"This email has already been taken!"
			self._errors["email"] = self.error_class([msg])
			del self.cleaned_data["email"]
		
		return self.cleaned_data

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(SettingsForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False

	def save(self, *args, **kwargs):
		profile = super().save(*args, **kwargs, commit=False)
		profile.user = self.user
		self.user.username = self.cleaned_data.get('username')
		avatar = self.cleaned_data.get('avatar')
		if avatar:
			profile.avatar = avatar
		profile.save()
		self.user.save()
		return profile

	

		
class AnswerForm(forms.ModelForm):

	class Meta:
		model = Answer
		fields = ['text']

		widgets = {
            'text': Textarea(attrs={'cols': 60,'rows': 8}),
        }

	def __init__(self, *args, **kwargs):
		self.profile = kwargs.pop('profile',None)
		self.qid = kwargs.pop('qid',None)
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False

	def save(self, *args, **kwargs):
		answer = super().save(*args, **kwargs, commit=False)
		answer.author = self.profile
		answer.question = self.qid 
		answer.save()
		return answer
