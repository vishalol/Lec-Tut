from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password',widget=forms.PasswordInput())

class PostForm(forms.Form):
	Post = forms.CharField( widget=forms.Textarea)

class CommentForm(forms.Form):
	Comment = forms.CharField(label='Comment', max_length=300)	