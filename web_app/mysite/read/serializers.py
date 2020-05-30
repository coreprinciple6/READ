from rest_framework import serializers
from .models import User, Student, Teacher, Classroom, Document, Enrolled_in, Student_Document, Student_Notice



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_student', 'is_teacher']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'photo']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user']

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['name', 'start_date', 'end_date', 'teacher']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'upload_date', 'classroom', 'document_file',]

class EnrolledInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrolled_in
        fields = ['student', 'classroom', 'status']

class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Document
        fields = ['enrolled_in', 'document', 'time_spent']

class StudentNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Notice
        fields = ['student', 'notice']






# class DocumentSerializer(serializers.ModelSerializer):
    # class Meta:
        # model =  Document
        # fields = ('id','name','upload_date','classroom')
