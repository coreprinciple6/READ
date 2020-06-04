from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, ClassroomSerializer, DocumentSerializer, EnrolledInSerializer, StudentDocumentSerializer, StudentNoticeSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Student, Teacher, Classroom, Document, Enrolled_in, Student_Notice, Student_Document


# the table_name_list views are the same for all classes with just a few changes depending on the model
# allowed methods are GET - for seeing a list of all table entries
# and POST - for posting a new entry

# the table_name_detail views are also very similar with minor changes for each model
# for these, GET, PUT and DELETE are the allowed methods

# the is_valid() method ensures the data entered is consistent with model requirements
# decorators at the beginning indicate allowed methods
# the Response() function renders nicely formatted html pages - the explorable REST API interface of the REST framework
# status codes are returned with the correct message using values from rest_framework.status


@api_view(['GET', 'POST'])
def user_list(request):
    if(request.method == 'GET'):
        # get a list of entries of this table, serialize it as json and return the response
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        # a new entry has been posted
        # deserialize the data
        # check if it's valid
        # and save
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, username):
    try:
        # get the entry in this table for which the user has the entered the primary key
        user = User.objects.get(username=username)
    except(User.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        # serialize the data for this entry and return it
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        # deserialize the data
        # perform validation
        # save the changes
        serializer = UserSerializer(user, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        # delete this user
        user.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def student_list(request):
    if(request.method == 'GET'):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except(Student.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = StudentSerializer(student, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        student.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def teacher_list(request):
    if(request.method == 'GET'):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def teacher_detail(request, pk):
    try:
        teacher = Teacher.objects.get(pk=pk)
    except(Teacher.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = TeacherSerializer(teacher, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        teacher.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def classroom_list(request):
    if(request.method == 'GET'):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def classroom_detail(request, pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
    except(Classroom.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = ClassroomSerializer(classroom, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        classroom.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def document_list(request):
    if(request.method == 'GET'):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def document_detail(request, pk):
    try:
        document = Document.objects.get(pk=pk)
    except(Document.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = DocumentSerializer(document)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = DocumentSerializer(document, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        document.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def enrolled_in_list(request):
    if(request.method == 'GET'):
        enrolled_ins = Enrolled_in.objects.all()
        serializer = EnrolledInSerializer(enrolled_ins, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = EnrolledInSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def enrolled_in_detail(request, pk):
    try:
        enrolled_in = Enrolled_in.objects.get(pk=pk)
    except(Enrolled_in.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = EnrolledInSerializer(enrolled_in)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = EnrolledInSerializer(enrolled_in, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        enrolled_in.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def student_document_list(request):
    if(request.method == 'GET'):
        student_documents = Student_Document.objects.all()
        serializer = StudentDocumentSerializer(student_documents, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = StudentDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def student_document_detail(request, pk):
    try:
        student_document = Student_Document.objects.get(pk=pk)
    except(Student_Document.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = StudentDocumentSerializer(student_document)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = StudentDocumentSerializer(student_document, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        student_document.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def student_notice_list(request):
    if(request.method == 'GET'):
        student_notices = Student_Notice.objects.all()
        serializer = StudentNoticeSerializer(student_notices, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = StudentNoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def student_notice_detail(request, pk):
    try:
        student_notice = Student_Notice.objects.get(pk=pk)
    except(Student_Notice.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = StudentNoticeSerializer(student_notice)
        return Response(serializer.data)
    elif(request.method == 'PUT'):
        serializer = StudentNoticeSerializer(student_notice, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'DELETE'):
        student_notice.delete();
        return Response(status=status.HTTP_204_NO_CONTENT)
