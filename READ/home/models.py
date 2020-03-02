from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)
    photo = models.ImageField(upload_to='home/students/', blank=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)

class Classroom(models.Model):
    name = models.CharField(max_length = 100, default="", blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False)

class Document(models.Model):
    upload_date = models.DateField(blank=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False)
    document_file = models.FileField(upload_to='home/documents/', null=True, blank=False)

class Student_Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, blank=False)
    time_spent = models.TimeField(blank=False)
    pages_read = models.IntegerField(default=0, blank=False)


class Enrolled_in(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False)
    enrolled_status = models.BooleanField(default=False, blank=False)



