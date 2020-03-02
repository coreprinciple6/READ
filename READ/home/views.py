from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegistrationForm, AddClassroomForm
from .models import User, Student, Teacher, Classroom, Document, Student_Document, Enrolled_in
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test

# ===============================================
# Miscellaneous functions
# ===============================================
def user_is_student(user):
    return user.is_student

def user_is_teacher(user):
    return user.is_teacher

def user_not_admin(user):
    return not user.is_superuser

def user_is_admin(user):
    return user.is_superuser
# ===============================================
# Common views
# ===============================================
def index(request):
    return HttpResponseRedirect(reverse('login_view'))

@login_required
@user_passes_test(user_is_admin)
def admin_redirected_view(request):
    return HttpResponse('<h1>You are logged in as admin.<br>Logout as admin to log in as a regular user.</h1>')

@login_required
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def logged_in_view(request):
    if(request.user.is_superuser):
        return HttpResponseRedirect(reverse('admin_redirected_view'))
    if(request.user.is_teacher):
        return HttpResponseRedirect(reverse('teacher_classes_view'))
    else:
        assert request.user.is_student == True
        return HttpResponseRedirect(reverse('student_classes_view'))

@login_required
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))

@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
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
    return render(request, 'home/login.html', {'form': form, 'error_message': error_message})

@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def register_view(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('logged_in_view'))
    if(request.method == 'POST'):
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            type_of_user = form.cleaned_data['type_of_user']
            user = form.save(commit=False)
            if(type_of_user == 'student'):
                user.is_student = True
                user.set_password(user.password)
                student = Student(user=user)
                user.save()
                student.save()
            else:
                assert type_of_user == 'teacher'
                user.is_teacher = True
                user.set_password(user.password)
                teacher = Teacher(user=user)
                user.save()
                teacher.save()

            return HttpResponseRedirect(reverse('login_view'))
    else:
        form = RegistrationForm()
    return render(request, 'home/register.html', {'form': form})


# ===============================================
# Teacher views
# ===============================================
@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def teacher_classes_view(request):
    go_to_add_class = request.POST.get('add_class', '0')
    if(go_to_add_class == '1'):
        return HttpResponseRedirect(reverse('teacher_adds_classroom_view'))

    cur_teacher = Teacher.objects.get(user_id=request.user.id)
    try:
        classes = Classroom.objects.filter(teacher_id=cur_teacher.user_id)
    except(Classroom.DoesNotExist):
        classes = None

    return render(request, 'home/teacher/teacher_classes.html', {'classes' : classes})


@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def teacher_profile_view(request):
    return render(request, 'home/teacher/teacher_profile.html')


@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def teacher_adds_classroom_view(request):
    if(request.method == 'POST'):
        form = AddClassroomForm(request.POST)
        if(form.is_valid()):
            classroom = form.save(commit=False)
            classroom.teacher = Teacher(user=request.user)
            print(classroom)
            classroom.save()
            return HttpResponseRedirect(reverse('teacher_classes_view'))
    else:
        form = AddClassroomForm()
    return render(request, 'home/teacher/teacher_adds_classroom.html', {'form' : form})
# ===============================================
# Student views
# ===============================================
@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def student_classes_view(request):
    return render(request, 'home/student/student_classes.html')


@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/home/admin_redirected')
def student_profile_view(request):
    return render(request, 'home/student/student_profile.html')
