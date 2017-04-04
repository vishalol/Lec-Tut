from django.conf.urls import url

from . import views

app_name='lectut'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^log/$', views.log, name='log'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^studentSignup/$', views.studentSignup, name='studentSignup'),
    url(r'^proffSignup/$', views.proffSignup, name='proffSignup'),
    url(r'^logo/$', views.logo, name='logo'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<course_id>[0-9]+)/course/$', views.coursepage, name='coursepage'),
	url(r'^profile/(?P<course_id>[0-9]+)/course/posting/$', views.posting, name='posting'),
	url(r'^profile/(?P<course_id>[0-9]+)/course/(?P<post_id>[0-9]+)/commenting/$', views.commenting, name='commenting'),   
    url(r'^(?P<username>[\w.@+-]+)/userprofile/$', views.userprofile, name='userprofile'),
    url(r'^profile/(?P<course_id>[0-9]+)/course/(?P<post_id>[0-9]+)/profilecommenting/$', views.profilecommenting, name='profilecommenting'),
    url(r'^homepage/$', views.homepage, name='homepage'),
]