from django.db import models

# Create your models here.


class Major(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    future_outlook = models.TextField()  # Brief on job market outlook


class Course(models.Model):
    major = models.ForeignKey(
        Major, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
