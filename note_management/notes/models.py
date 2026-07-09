from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):

    title=models.CharField(max_length=100)
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Note(models.Model):

    title=models.CharField(max_length=100)
    content=models.TextField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.title