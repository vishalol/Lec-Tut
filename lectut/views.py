from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.


#login page
def index(request):
    if request.user.is_authenticated():
        user = request.user
        if(hasattr(user, 'student')):
            student = user.student
            return HttpResponseRedirect(reverse('lectut:profile'))
        else:
            proff = user.proff
            return HttpResponseRedirect(reverse('lectut:profile'))
    form = LoginForm()
    return render(request, 'lectut/index.html', {'form': form})


# different course pages
def coursepage(request, course_id):
    if request.user.is_authenticated():
        form1 = PostForm()
        form2 = CommentForm()
        course = get_object_or_404(Course, pk=course_id)
        return render(request, 'lectut/course.html', {'course': course,  'userid': request.user.id, 'form1': form1, 'form2':form2})
    else:
        messages.error(request, 'You have to login 1st')
        return HttpResponseRedirect(reverse('lectut:index'))
        

# profile page shown just after login
def profile(request ):
    if request.user.is_authenticated():
        user = request.user
        latest_post = Post.objects.order_by('-pub_time')[:5]
        form2 = CommentForm()
        
        if(hasattr(user, 'student')):
            student = user.student
            list1 = student.courses.all()
            postlist = []
            recentpostlist = [];
            for course in list1:
                post = course.post_set.all()
                for pos in post:
                    postlist.append(pos)
            recentpostlist = sorted(postlist, key=lambda x: x.pub_time, reverse=True)[:5]   
            return render(request, 'lectut/profile.html', {'user': student, 'latestpost':recentpostlist,'userid': user.id, 'form2':form2})
        else:
            proff = user.proff
            list1 = proff.courses.all()
            postlist = []
            recentpostlist = [];
            for course in list1:
                post = course.post_set.all()
                for pos in post:
                    postlist.append(pos)
            recentpostlist = sorted(postlist, key=lambda x: x.pub_time, reverse=True)[:5]
            return render(request, 'lectut/profile.html', {'user':proff, 'latestpost':recentpostlist,'userid': user.id, 'form2':form2})

    else:
        messages.error(request, 'You have to login 1st')
        return HttpResponseRedirect(reverse('lectut:index'))    


# for loggin in user and redirecting to profile page upon successful login
def log(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('lectut:profile'))
            else :
                form = LoginForm()
                return render(request, 'lectut/index.html',{'form':form, 'error_message':"Incorrect Credentials"})
    else:
        return HttpResponseRedirect(reverse('lectut:index'))


# log out the user
def logo(request):
    logout(request)
    return HttpResponseRedirect(reverse('lectut:index'))


# for handling the posts added from coursepage
def posting(request, course_id):
        if request.method == 'POST':
            user = request.user
            if(hasattr(user, 'student')):
                student = user.student
                course1 = student.courses.all()
            else:
                proff = user.proff
                course1 = proff.courses.all()
            course = get_object_or_404(Course, pk=course_id)
            if course in course1:
                if(len(request.FILES) != 0):
                    course.post_set.create(post=request.POST['Post'], poster=user.username, docfile = request.FILES['docfile'])
                else:
                    course.post_set.create(post=request.POST['Post'], poster=user.username)   
                return HttpResponseRedirect(reverse('lectut:coursepage', args=(course_id)))
            else:
                messages.error(request, 'You cannot post in this course')
                return HttpResponseRedirect(reverse('lectut:coursepage', args=(course_id))) 

# handling the comments on posts from coursepage
def commenting(request, course_id, post_id):
        if request.method == 'POST':
            user = request.user
            if(hasattr(user, 'student')):
                student = user.student
                course = student.courses.all()
            else:
                proff = user.proff
                course = proff.courses.all()
                    
            course1 = get_object_or_404(Course, pk=course_id)
            post = get_object_or_404(Post, pk=post_id)
            if course1 in course:
                post.comment_set.create(comment=request.POST['Comment'], commenter=user.username)
                return HttpResponseRedirect(reverse('lectut:coursepage', args=(course_id))) 
            else:
                messages.error(request, 'You cannot comment on this course')
                return HttpResponseRedirect(reverse('lectut:coursepage', args=(course_id)))

# handling the comments on posts from profilepage
def profilecommenting(request, course_id, post_id):
        if request.method == 'POST':
            user = request.user
            if(hasattr(user, 'student')):
                student = user.student
                course = student.courses.all()
            else:
                proff = user.proff
                course = proff.courses.all()
                    
            course1 = get_object_or_404(Course, pk=course_id)
            post = get_object_or_404(Post, pk=post_id)
            if course1 in course:
                post.comment_set.create(comment=request.POST['Comment'], commenter=user.username)
                return HttpResponseRedirect(reverse('lectut:profile'))  
            else:
                messages.error(request, 'You cannot comment on this course')
                return HttpResponseRedirect(reverse('lectut:profile'))              

# displaying profile of different users
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



def homepage(request):
    return HttpResponseRedirect(reverse('lectut:profile'))


def like(request):
    if request.method == 'POST':
        user = request.user
        postId = request.POST['post_id']
        post = get_object_or_404(Post, pk = postId)
        if post.likes.filter(id = user.id).exists():
            post.likes.remove(user)
            likecounter = 0
            unlikecounter = 0
        elif post.unlikes.filter(id = user.id).exists():
            post.unlikes.remove(user)
            post.likes.add(user)
            likecounter = 1
            unlikecounter = 0  
        else:
            post.likes.add(user)
            likecounter = 1
            unlikecounter = 0
            
    ctx = {'likes_count': post.likes.count(), 'unlikes_count': post.unlikes.count(), 'like': likecounter, 'unlike': unlikecounter}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def unlike(request):
    if request.method == 'POST':
        user = request.user
        postId = request.POST['post_id']
        post = get_object_or_404(Post, id = postId)
        if post.unlikes.filter(id = user.id).exists():
            post.unlikes.remove(user)
            likecounter = 0
            unlikecounter = 0
        elif post.likes.filter(id = user.id).exists():
            post.likes.remove(user)
            post.unlikes.add(user)
            likecounter = 0
            unlikecounter = 1  
        else:
            post.unlikes.add(user)
            likecounter = 0
            unlikecounter = 1
    ctx = {'likes_count': post.likes.count(),'unlikes_count': post.unlikes.count(), 'like': likecounter, 'unlike': unlikecounter}
    return HttpResponse(json.dumps(ctx), content_type='application/json')  


# views for creaing new users
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            login(request, user)
            if (request.POST['typ']=='Student'):
                return HttpResponseRedirect(reverse('lectut:studentSignup'))
            else:
                return HttpResponseRedirect(reverse('lectut:proffSignup'))  
        else :
            return render(request, 'lectut/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'lectut/signup.html', {'form': form})


def studentSignup(request):
    if request.method == 'POST':
        form = StudentSignup(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('lectut:profile'))
        else:
            return render(request, 'lectut/studentsignup.html', {'form': form})
            #return HttpResponseRedirect(reverse('lectut:studentSignup'))   
    form = StudentSignup()      
    return render(request, 'lectut/studentsignup.html', {'form': form})     


def proffSignup(request):
    if request.method == 'POST':
        form = ProffSignup(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('lectut:profile'))
        else:
            return render(request, 'lectut/proffsignup.html', {'form': form})
            #return HttpResponseRedirect(reverse('lectut:proffSignup')) 
    form = ProffSignup()
    return render(request, 'lectut/proffsignup.html', {'form': form})       

