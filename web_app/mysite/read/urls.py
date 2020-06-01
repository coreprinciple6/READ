from django.urls import path

from . import views, api_views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logged_in/', views.logged_in_view, name='logged_in_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('admin_redirected/', views.admin_redirected_view, name='admin_redirected_view'),

    path('teacher/classes/', views.teacher_classes_view, name='teacher_classes_view'),
    path('teacher/classes/add/', views.teacher_adds_classroom_view, name='teacher_adds_classroom_view'),
    path('teacher/classes/<slug:class_name>/', views.teacher_specific_class_view, name='teacher_specific_class_view'),
    path('teacher/classes/<slug:class_name>/add/', views.teacher_adds_document_view, name='teacher_adds_document_view'),
    path('teacher/classes/<slug:class_name>/stats/', views.teacher_stats_view, name='teacher_stats_view'),
    path('teacher/classes/<slug:class_name>/<slug:file_name>/view/', views.teacher_file_view, name='teacher_file_view'),


    path('student/classes/', views.student_classes_view, name='student_classes_view'),
    path('student/photo/', views.student_photo_view, name='student_photo_view'),
    path('student/classes/join/', views.student_join_class_view, name='student_join_class_view'),
    path('student/notices/', views.student_notices_view, name='student_notices_view'),
    path('student/classes/<slug:class_name>/', views.student_specific_class_view, name='student_specific_class_view'),
    path('student/classes/<slug:class_name>/<slug:file_name>/authenticate/', views.student_authenticate_view, name='student_authenticate_view'),
    path('student/classes/<slug:class_name>/<slug:file_name>/view/', views.student_file_view, name='student_file_view'),

    # google-sign-in
    path('google_sign_in/', views.google_sign_in_view, name='google_sign_in_view'),


    # API paths
    path('api/users/', api_views.user_list, name='user_list'),
    path('api/users/<slug:username>', api_views.user_detail, name='user_detail'),

    path('api/students/', api_views.student_list, name='student_list'),
    path('api/students/<int:pk>', api_views.student_detail, name='student_detail'),

    path('api/teachers/', api_views.teacher_list, name='teacher_list'),
    path('api/teachers/<int:pk>', api_views.teacher_detail, name='teacher_detail'),

    path('api/classrooms/', api_views.classroom_list, name='classroom_list'),
    path('api/classrooms/<int:pk>', api_views.classroom_detail, name='classroom_detail'),

    path('api/documents/', api_views.document_list, name='document_list'),
    path('api/documents/<int:pk>', api_views.document_detail, name='document_detail'),

    path('api/enrolled_ins/', api_views.enrolled_in_list, name='enrolled_in_list'),
    path('api/enrolled_ins/<int:pk>', api_views.enrolled_in_detail, name='enrolled_in_detail'),

    path('api/student_documents/', api_views.student_document_list, name='student_document_list'),
    path('api/student_documents/<int:pk>', api_views.student_document_detail, name='student_document_detail'),

    path('api/student_notices/', api_views.student_notice_list, name='student_notice_list'),
    path('api/student_notices/<int:pk>', api_views.student_notice_detail, name='student_notice_detail'),

]
