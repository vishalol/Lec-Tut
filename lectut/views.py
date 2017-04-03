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
	if request.user.is_authenticated():
		form1 = PostForm()
		form2 = CommentForm()
		course = get_object_or_404(Course, pk=course_id)
		return render(request, 'lectut/course.html', {'course': course,  'userid': user_id, 'form1': form1, 'form2':form2})
	else:
		messages.error(request, 'You have to login 1st')
		return HttpResponseRedirect(reverse('lectut:index'))
		


def profile(request, user_id, ):
	if request.user.is_authenticated():
		user = get_object_or_404(User, pk=user_id)
		latest_post = Post.objects.order_by('-pub_time')[:5]
		form2 = CommentForm()
		
		if(hasattr(user, 'student')):
			student = user.student
			list1 = student.courses.all()
			list2 = []
			list3 = []
			for course in list1:
				pos = course.post_set.all().order_by('-pub_time')[:1]
				if(pos):
					list2.append(pos[0])

					list3.append(course)

			return render(request, 'lectut/profile.html', {'user': student, 'latestpost':zip(list2, list3),'userid': user_id, 'form2':form2})
		else:
			proff = user.proff
			list1 = proff.courses.all()
			list2 = []
			list3 = []
			for course in list1:
				pos = course.post_set.all().order_by('-pub_time')[:1]
				if(pos):
					list2.append(pos[0])

					list3.append(course)
			return render(request, 'lectut/profile.html', {'user':proff, 'latestpost':zip(list2, list3),'userid': user_id, 'form2':form2})

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



def commenting(request,user_id, course_id, post_id):
		if request.method == 'POST':
			user = get_object_or_404(User, pk=user_id)
			post = get_object_or_404(Post, pk=post_id)
			post.comment_set.create(comment=request.POST['Comment'], commenter=user.username)
			return HttpResponseRedirect(reverse('lectut:coursepage', args=(user.id,course_id)))	



def userprofile(request, username):
	if request.user.is_authenticated():
		user = get_object_or_404(User, username=username)
		if(hasattr(user, 'student')):
			student = user.student
			return render(request, 'lectut/userprofile.html', {'user': student, 'userid': user.id, 'typ':'stud'})
		else:
			proff = user.proff
			return render(request, 'lectut/userprofile.html', {'user':proff, 'userid': user.id})
	else:
		messages.error(request, 'You have to login 1st')
		return HttpResponseRedirect(reverse('lectut:index'))