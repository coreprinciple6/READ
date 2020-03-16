from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
from django.urls import reverse
from .forms import LoginForm, RegistrationForm, AddClassroomForm, AddDocumentForm, StudentUploadPhotoForm
from .models import User, Student, Teacher, Classroom, Document, Student_Document, Enrolled_in, Student_Notice
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.conf import settings
import os.path
from os import path
from . import face_authenticate

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

def student_enrolled_in_class(user, class_name):
    try:
        student = Student.objects.get(user=user)
    except:
        raise Exception('student not found')
    try:
        classroom = Classroom.objects.get(name=class_name)
    except:
        raise Exception('classroom not found')
    try:
        enrolled_in_class = Enrolled_in.objects.get(student=student, classroom=classroom)
        return enrolled_in_class.status
    except:
        return False
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
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def logged_in_view(request):
    if(request.user.is_superuser):
        return HttpResponseRedirect(reverse('admin_redirected_view'))
    if(request.user.is_teacher):
        return HttpResponseRedirect(reverse('teacher_classes_view'))
    if(request.user.is_student):
        return HttpResponseRedirect(reverse('student_classes_view'))
    else:
        #assert request.user.is_student == True
        #return HttpResponseRedirect(reverse('student_classes_view'))
        return HttpResponseRedirect(reverse('test_view'))

@login_required
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))

@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
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

@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
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
    return render(request, 'read/register.html', {'form': form})


# ===============================================
# Teacher views
# ===============================================
@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def teacher_classes_view(request):
    action = request.POST.get('action')
    if(action == 'add_class'):
        return HttpResponseRedirect(reverse('teacher_adds_classroom_view'))
    elif(action == 'delete'):
        class_name = request.POST.get('class_name')
        assert class_name is not None
        _class = Classroom.objects.get(name=class_name)
        _class.delete()
    else:
        assert action is None

    cur_teacher = Teacher.objects.get(user_id=request.user.id)
    try:
        classes = Classroom.objects.filter(teacher_id=cur_teacher.user_id)
        pending_requests = [0 for x in range(classes.count())]
        for idx, _class in enumerate(classes):
            pending_requests[idx] = Enrolled_in.objects.filter(classroom=_class, status = False).count()
    except(Classroom.DoesNotExist):
        classes = None
        pending_requests = None

    return render(request, 'read/teacher/teacher_classes.html', {'classes' : classes, 'pending_requests' : pending_requests})


@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def teacher_profile_view(request):
    return render(request, 'read/teacher/teacher_profile.html')


@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def teacher_adds_classroom_view(request):
    if(request.method == 'POST'):
        form = AddClassroomForm(request.POST)
        if(form.is_valid()):
            classroom = form.save(commit=False)
            classroom.teacher = Teacher(user=request.user)
            classroom.save()
            return HttpResponseRedirect(reverse('teacher_classes_view'))
    else:
        form = AddClassroomForm()
    return render(request, 'read/teacher/teacher_adds_classroom.html', {'form' : form})



@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def teacher_specific_class_view(request, class_name):
    cur_class = get_object_or_404(Classroom, name=class_name)
    if(request.method == 'POST'):
        print(request.POST)
        action = request.POST.get('action')
        if(action == "Add document"):
            return  HttpResponseRedirect(reverse('teacher_adds_document_view', kwargs={'class_name': class_name}))
        elif(action == "Delete Document"):
            doc_to_delete = request.POST.get('name')
            assert doc_to_delete is not None
            ret = Document.objects.get(classroom=cur_class, name=doc_to_delete).delete()
            # an object of type 'read.Document' is deleted
            assert ret[1]['read.Document'] == 1
        elif(action == 'Approve'):
            student_to_enroll = request.POST.get('student_name')
            assert student_to_enroll is not None
            print(f'SSTDNET TO ENROLL {student_to_enroll}')
            student = Student.objects.get(user__username=student_to_enroll)
            enrolled_in_instance = Enrolled_in.objects.get(student=student, classroom=cur_class)
            assert enrolled_in_instance.status == False
            assert enrolled_in_instance is not None
            enrolled_in_instance.status = True
            enrolled_in_instance.save()
            notice = Student_Notice(student=student, notice=f"Request to join {cur_class.name} has been approved")
            notice.save()
        elif(action == 'Decline'):
            student_to_decline = request.POST.get('student_name')
            student = Student.objects.get(user__username=student_to_decline)
            enrolled_in_instance = Enrolled_in.objects.get(student=student, classroom=cur_class)
            assert enrolled_in_instance is not None
            assert enrolled_in_instance.status == False
            enrolled_in_instance.delete()
            notice = Student_Notice(student=student, notice=f"Request to join {cur_class.name} has been denied")
            notice.save()
        elif(action == 'Remove Student'):
            student_name = request.POST.get('student_name')
            student = Student.objects.get(user__username=student_name)
            Enrolled_in.objects.get(classroom = cur_class, student=student).delete()
            notice = Student_Notice(student=student, notice=f"You have been removed from {cur_class.name}")
            notice.save()
        else:
            assert 1 == 0

    try:
        enrolled_students_pks = Enrolled_in.objects.filter(classroom=cur_class, status=True).values_list('student', flat=True)
        enrolled_students = Student.objects.filter(pk__in=enrolled_students_pks)
    except:
        enrolled_students = None

    try:
        pending_requests = Enrolled_in.objects.filter(classroom=cur_class, status=False)
    except:
        pending_requests = None

    try:
        uploaded_documents = Document.objects.filter(classroom=cur_class)
    except(Document.DoesNotExist):
        uploaded_documents = None

    print(f'enrolled_students: {enrolled_students}')
    print(f'pending_requests: {pending_requests}')


    return render(request, 'read/teacher/teacher_specific_class.html', {'class' : cur_class, 'enrolled_students' : enrolled_students, 'uploaded_documents' : uploaded_documents, 'pending_requests' : pending_requests})


@login_required
@user_passes_test(user_is_teacher)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def teacher_adds_document_view(request, class_name):
    cur_class = Classroom.objects.get(name=class_name)
    if(request.method == 'POST'):
        form = AddDocumentForm(request.POST, request.FILES)
        if(form.is_valid()):
            document = form.save(commit=False)
            if(Document.objects.filter(name=document.name, classroom=cur_class).exists() == False):
                document.upload_date = datetime.today()
                document.classroom = cur_class
                document.save()
                return HttpResponseRedirect(reverse('teacher_specific_class_view', args=[class_name]))
            else:
                form.add_error('name', 'Document with name already exists within this class')
    else:
        form = AddDocumentForm()
    return render(request, 'read/teacher/teacher_adds_document.html', {'form' : form, 'class_name' : class_name})

# ===============================================
# Student views
# ===============================================
@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_classes_view(request):
    student = Student(user=request.user)
    if(request.method == 'POST'):
        action = request.POST.get('action')
        if(action == 'Leave Class'):
            class_name = request.POST.get('class_name')
            _class = Classroom.objects.get(name=class_name)
            assert _class is not None
            enrolled_in_instance = Enrolled_in.objects.get(student=student, classroom=_class)
            enrolled_in_instance.delete()

    try:
        enrolled_classes_pks = Enrolled_in.objects.filter(student=student, status=True).values_list('classroom', flat=True)
        enrolled_classes = Classroom.objects.filter(pk__in=enrolled_classes_pks)
    except:
        enrolled_classes = None

    return render(request, 'read/student/student_classes.html', {'enrolled_classes' : enrolled_classes})

@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_join_class_view(request):
    student = Student(user = request.user)
    if(request.method == 'POST'):
        action = request.POST.get('action')
        class_name = request.POST.get('class_name')
        classroom = Classroom.objects.get(name=class_name)
        assert class_name is not None
        assert action is not None
        if(action == 'Join Class'):
            enrolled_in_instance = Enrolled_in(student=student, classroom=classroom, status=False)
            enrolled_in_instance.save()
        else:
            raise Exception('action error in student_join_class_view')



    try:
        joined_classes_pks = Enrolled_in.objects.filter(student=student, status=True).values_list('classroom', flat=True)
        joined_classes = Classroom.objects.filter(pk__in=joined_classes_pks)
    except:
        joined_classes = None

    try:
        if(joined_classes is None):
            not_joined_classes = Classroom.objects.all()
        else:
            not_joined_classes = Classroom.objects.exclude(pk__in=joined_classes)


        class_join_status = [0 for x in range(len(not_joined_classes))]
        for idx, _class in enumerate(not_joined_classes):
            try:
                status = Enrolled_in.objects.get(student=student, classroom=_class).status
                try:
                    assert status is False
                except:
                    raise Exception('Status should be false')
                status = 'Pending Approval'
            except:
                status = None
                status = 'Not joined'
            class_join_status[idx] = status



    except:
        not_joined_classes = None
        class_join_status = None

    return render(request, 'read/student/student_join_class.html', {'not_joined_classes' : not_joined_classes, 'class_join_status' : class_join_status})




@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_notices_view(request):
    student = Student.objects.get(user=request.user)
    if(request.method == 'POST'):
        notice_pk = int(request.POST.get('notice_pk'))
        assert notice_pk is not None
        notice = Student_Notice.objects.get(pk=notice_pk)
        notice.delete()


    try:
        notices = Student_Notice.objects.filter(student=student)
    except Exception as e:
        notices = None
    return render(request, 'read/student/student_notices.html', {'notices' : notices})




@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_specific_class_view(request, class_name):
    if(student_enrolled_in_class(request.user, class_name) == False):
        return HttpResponseRedirect(reverse('student_classes_view'))
    classroom = Classroom.objects.get(name=class_name)
    try:
        docs = Document.objects.filter(classroom=classroom)
    except:
        docs = None

    return render(request, 'read/student/student_specific_class.html', {'class' : classroom, 'docs' : docs})


@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_authenticate_view(request, class_name, file_name):
    if(student_enrolled_in_class(request.user, class_name) == False):
        return HttpResponseRedirect(reverse('student_classes_view'))


    student = Student.objects.get(user=request.user)
    photo_not_uploaded = True
    try:
        photo_path = student.photo.path
        if(path.exists(photo_path) == False):
            photo_path = None
        else:
            photo_not_uploaded = False
    except:
        photo_path = None

    authenticated = False
    if(photo_not_uploaded == False):
        name = student.user.first_name + ' ' + student.user.last_name
        authenticate_result = face_authenticate.facial_recognition(name, photo_path)
        authenticated = 0
        if(authenticate_result == 0):
            authenticated = 0
        elif(authenticate_result == 1):
            authenticated = 1
            return HttpResponseRedirect(reverse('student_file_view', args=[class_name, file_name]))
        else:
            assert authenticate_result == 2
            authenticated = 2


    return render(request, 'read/student/student_authentication.html', {'photo_not_uploaded' : photo_not_uploaded, 'authenticated' : authenticated})



@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_file_view(request, class_name, file_name):
    classroom = Classroom.objects.get(name=class_name)
    if(student_enrolled_in_class(request.user, class_name) == False):
        return HttpResponseRedirect(reverse('student_classes_view'))
    try:
        try:
            doc = Document.objects.get(classroom=classroom, name=file_name)
        except:
            raise Exception('Error retrieving file')
        path = settings.MEDIA_ROOT + str(doc.document_file)
        return FileResponse(open(path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('File does not exist')


@login_required
@user_passes_test(user_is_student)
@user_passes_test(user_not_admin, login_url='/read/admin_redirected')
def student_profile_view(request):
    student = Student.objects.get(user=request.user)
    if(request.method == 'POST'):
        action = request.POST.get('action')
        if(action == 'Submit'):
            form = StudentUploadPhotoForm(request.POST, request.FILES)
            if(form.is_valid()):
                cur_student = form.save(commit=False)
                student.photo = cur_student.photo
                student.save()
        else:
            assert action == 'Remove Photo'
            form = StudentUploadPhotoForm()
            student.photo = None
            student.save()
    else:
        form = StudentUploadPhotoForm()

    try:
        photo_url = student.photo.url
        photo_path = student.photo.path
        if(path.exists(photo_path) == False):
            photo_url = None
    except:
        photo_url = None

    print(photo_url)
    return render(request, 'read/student/student_profile.html', {'form' : form, 'photo_url' : photo_url})


#--------------------------------------------------


def test_view(request):

    return render(request, 'read/base_profile.html')

def sbase_view(request) :
    fish = request.user.username
    print(fish)
    check = User.objects.get(username=fish)
    check.is_student = True
    check.save()
    return render(request, 'read/base_profile.html')

    #return HttpResponseRedirect(reverse('logged_in_view'))