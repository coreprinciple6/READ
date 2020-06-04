from rest_framework import serializers
from .models import User, Student, Teacher, Classroom, Document, Enrolled_in, Student_Document, Student_Notice


# all serializers follow the same pattern.
# each serializer corresponds to a model
# this is defined by the value of the model variable within the meta data of the serializers
# all fields were chosen to be serialized except the auto generated id field for student and teacher because we use the user value as the primary key for these models
# these serializers perform serialization as well as deserialization when PUT or POST requests are made
# calling serializer.save() ensures the model constraints are maintained and then saves the new entry or updates an existing one

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_student', 'is_teacher']


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
        fields = ['id', 'name', 'start_date', 'end_date', 'teacher']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'upload_date', 'classroom', 'document_file',]

class EnrolledInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrolled_in
        fields = ['id', 'student', 'classroom', 'status']

class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Document
        fields = ['id', 'enrolled_in', 'document', 'time_spent']

class StudentNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Notice
        fields = ['id', 'student', 'notice']
