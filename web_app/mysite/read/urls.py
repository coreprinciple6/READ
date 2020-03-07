from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logged_in/', views.logged_in_view, name='logged_in_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('admin_redirected/', views.admin_redirected_view, name='admin_redirected_view'),

    path('teacher/classes/', views.teacher_classes_view, name='teacher_classes_view'),
    path('teacher/profile/', views.teacher_profile_view, name='teacher_profile_view'),
    path('teacher/classes/add/', views.teacher_adds_classroom_view, name='teacher_adds_classroom_view'),
    path('teacher/classes/<slug:class_name>/', views.teacher_specific_class_view, name='teacher_specific_class_view'),
    path('teacher/classes/<slug:class_name>/add/', views.teacher_adds_document_view, name='teacher_adds_document_view'),

    path('student/classes/', views.student_classes_view, name='student_classes_view'),
    path('student/profile/', views.student_profile_view, name='student_profile_view'),
    path('student/classes/join/', views.student_join_class_view, name='student_join_class_view'),
    path('student/notices/', views.student_notices_view, name='student_notices_view'),
    path('student/classes/<slug:class_name>/', views.student_specific_class_view, name='student_specific_class_view'),
    path('student/classes/<slug:class_name>/<slug:file_name>/authenticate/', views.student_authenticate_view, name='student_authenticate_view'),
    path('student/classes/<slug:class_name>/<slug:file_name>/view/', views.student_file_view, name='student_file_view'),
]