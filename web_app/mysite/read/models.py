from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(null=True)
    is_teacher = models.BooleanField(null=True)

    def __str__(self):
        return f'''
            username: {self.username}
            email: {self.email}
            first_name: {self.first_name}
            last_name: {self.last_name}
            is_student: {self.is_student}
            is_teacher: {self.is_teacher}
            password_hash: {self.password}
        '''

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)
    photo = models.ImageField(upload_to='read/students/', blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)

class Classroom(models.Model):
    name = models.SlugField(max_length = 100, blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False)
    def __str__(self):
        return f'''
            class_name: {self.name}
            teacher: {self.teacher}
        '''

class Document(models.Model):
    name = models.SlugField(max_length = 100, default="", blank=False)
    upload_date = models.DateField(blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False)
    document_file = models.FileField(upload_to='read/documents/', null=True, blank=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return f'doc name : {self.name}\ndoc_file: {self.document_file}'

    class Meta:
        unique_together = (('name', 'classroom'))

class Student_Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, blank=False)
    time_spent = models.TimeField(blank=False)
    pages_read = models.IntegerField(default=0, blank=False)

    class Meta:
        unique_together = (('student', 'document'))

class Enrolled_in(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False)
    # status : {False => pending_approval, True => joined}
    status = models.BooleanField(default=False, blank=False)
    class Meta:
        unique_together = (('student', 'classroom'))

    def __str__(self):
        return f'''
        student: {self.student.user}
        classroom : {self.classroom.name}
        status: {self.status}
        '''

class Student_Notice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    notice = models.CharField(max_length=300, blank=False)


