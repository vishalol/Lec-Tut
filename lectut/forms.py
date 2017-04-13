import re
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist

TITLE_CHOICES = (
    ('Student', 'Student'),
    ('Proffessor', 'Proffessor'),
)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password',widget=forms.PasswordInput())

class PostForm(forms.Form):
	Post = forms.CharField( widget=forms.Textarea)

class CommentForm(forms.Form):
	Comment = forms.CharField(label='Comment', max_length=300)

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='Email')
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password (Again)',widget=forms.PasswordInput())
	typ = forms.CharField(max_length=20,widget=forms.Select(choices=TITLE_CHOICES))

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')

	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')


class StudentSignup(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'branch', 'year', 'courses']
        exclude = ['user']

class ProffSignup(forms.ModelForm):
    class Meta:
        model = Proff
        fields = ['name', 'courses']
        exclude = ['user']
                		