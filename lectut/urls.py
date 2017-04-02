from django.conf.urls import url

from . import views

app_name='lectut'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^log/$', views.log, name='log'),
    url(r'^logo/$', views.logo, name='logo'),
    url(r'^(?P<user_id>[0-9]+)/profile/$', views.profile, name='profile'),
    url(r'^(?P<user_id>[0-9]+)/profile/(?P<course_id>[0-9]+)/course/$', views.coursepage, name='coursepage'),
	url(r'^(?P<user_id>[0-9]+)/profile/(?P<course_id>[0-9]+)/course/posting/$', views.posting, name='posting'),   
]