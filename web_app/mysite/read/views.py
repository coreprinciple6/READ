from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegistrationForm
from .models import User, Student, Teacher, Classroom, Document, Student_Document, Enrolled_in
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test

# ===============================================
# Miscellaneous functions
# ===============================================
def student_check(user):
    return user.is_student

def teacher_check(user):
    return user.is_teacher

# ===============================================
# Common views
# ===============================================
def index(request):
    return HttpResponseRedirect(reverse('login_view'))

@login_required
def logged_in_view(request):
    if(request.user.is_teacher):
        return HttpResponseRedirect(reverse('teacher_classes_view'))
    else:
        assert request.user.is_student
        return HttpResponseRedirect(reverse('student_classes_view'))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))

def login_view(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('logged_in_view'))

    error_message = None
    if(request.method == 'POST'):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if(user is None):
                error_message = "Incorrect username or password."
            else:
                login(request, user)
                return HttpResponseRedirect(reverse('logged_in_view'))
    else:
        form = LoginForm()
    return render(request, 'read/login.html', {'form': form, 'error_message': error_message})

def register_view(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('logged_in_view'))
    if(request.method == 'POST'):
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            type_of_user = form.cleaned_data['type_of_user']
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            if(User.objects.filter(email=email).exists()):
                error_message = 'Email already exists.'
                return render(request, 'read/register.html', {'form': form, 'error_message' : error_message})
            elif(type_of_user == 'student'):
                user.is_student = True
                user.set_password(user.password)
                student = Student(user=user)
                user.save()
                student.save()
            else:
                user.is_teacher = True
                user.set_password(user.password)
                teacher = Teacher(user=user)
                user.save()
                teacher.save()

            return HttpResponseRedirect(reverse('login_view'))
    else:
        form = RegistrationForm()
    return render(request, 'read/register.html', {'form': form})


# ===============================================
# Teacher views
# ===============================================
@login_required
@user_passes_test(teacher_check)
def teacher_classes_view(request):
    cur_teacher = Teacher.objects.get(user_id=request.user.id)
    try:
        classes = Classroom.objects.filter(teacher_id=cur_teacher.user_id)
    except(Classroom.DoesNotExist):
        classes = None

    return render(request, 'read/teacher/teacher_classes.html', {'classes' : classes})


@login_required
@user_passes_test(teacher_check)
def teacher_profile_view(request):
    return render(request, 'read/teacher/teacher_profile.html')


# ===============================================
# Student views
# ===============================================
@login_required
@user_passes_test(student_check)
def student_classes_view(request):
    return render(request, 'read/student/student_classes.html')


@login_required
@user_passes_test(student_check)
def student_profile_view(request):
    return render(request, 'read/student/student_profile.html')
