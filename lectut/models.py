from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    courseName = models.CharField(max_length=200)
    def __str__(self):
        return self.courseName


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=200)
    enrollment = models.CharField(max_length=8)
    branch = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    courses = models.ManyToManyField('Course')
    def __str__(self):
        return self.name


class Proff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=200)
    courses = models.ManyToManyField('Course') 
    def __str__(self):
        return self.name



class Post(models.Model):
    post = models.CharField(max_length=300)
    poster = models.CharField(max_length=200)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True, null=True)      
    pub_time = models.DateTimeField(auto_now_add=True)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.post    


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    pub_time = models.DateTimeField(auto_now_add=True)
    commenter = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment

