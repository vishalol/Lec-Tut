from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from .forms import *
# Create your views here.

def index(request):
	if request.user.is_authenticated():
		user = request.user
		if(hasattr(user, 'student')):
			student = user.student
			return render(request, 'lectut/profile.html', {'user': student, 'userid': user.id})
		else:
			proff = user.proff
			return render(request, 'lectut/profile.html', {'user':proff, 'userid': user.id})
	form = LoginForm()
	return render(request, 'lectut/index.html', {'form': form})

def coursepage(request,user_id, course_id):
	form = PostForm()
	course = get_object_or_404(Course, pk=course_id)
	return render(request, 'lectut/course.html', {'course': course,  'userid': user_id, 'form': form})

def profile(request, user_id, ):
	if request.user.is_authenticated():
		user = get_object_or_404(User, pk=user_id)
		if(hasattr(user, 'student')):
			student = user.student
			return render(request, 'lectut/profile.html', {'user': student, 'userid': user_id})
		else:
			proff = user.proff
			return render(request, 'lectut/profile.html', {'user':proff, 'userid': user_id})

	else:
		messages.error(request, 'You have to login 1st')
		return HttpResponseRedirect(reverse('lectut:index'))	


def log(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('lectut:profile', args=(user.id,)))
			else :
				form = LoginForm()
				return render(request, 'lectut/index.html',{'form':form, 'error_message':"Incorrect Credentials"})
	else:
		return HttpResponseRedirect(reverse('lectut:index'))



def logo(request):
	logout(request)
	return HttpResponseRedirect(reverse('lectut:index'))

def posting(request,user_id, course_id):
		if request.method == 'POST':
			user = get_object_or_404(User, pk=user_id)
			course = get_object_or_404(Course, pk=course_id)
			course.post_set.create(post=request.POST['Post'], poster=user.username)
			return HttpResponseRedirect(reverse('lectut:coursepage', args=(user.id,course_id)))