from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(upload_to='read/students/', null=True, blank=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Classroom(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Document(models.Model):
    upload_date = models.DateField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='read/documents/')

class Student_Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    time_spent = models.TimeField()
    pages_read = models.IntegerField(default=0)


class Enrolled_in(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    enrolled_status = models.BooleanField(default=False)



