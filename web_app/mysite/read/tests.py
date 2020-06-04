from django.test import TestCase
from django.db.utils import IntegrityError
from .models import User, Student, Teacher, Classroom, Document, Enrolled_in, Student_Document, Student_Notice
from datetime import date



# model tests
class __str__Tests(TestCase):
    def setUp(self):
        self.userObj = User.objects.create(username="something", email="something@gmail.com", first_name="fname", last_name="lname", is_student=True, is_teacher=False)
        self.studentObj = Student.objects.create(user=self.userObj)
        self.teacherObj = Teacher.objects.create(user=self.userObj)
        self.classroomObj = Classroom.objects.create(name="class1", start_date=date(2019, 12, 4), end_date =date(2029, 12, 4), teacher=self.teacherObj)
        self.documentObj = Document.objects.create(name="doc", upload_date=date(2020, 2, 2), classroom=self.classroomObj, document_file='somepath')
        self.enrolled_in_obj = Enrolled_in.objects.create(student=self.studentObj, classroom=self.classroomObj, status=True)
        self.student_doc_obj = Student_Document.objects.create(enrolled_in=self.enrolled_in_obj, document=self.documentObj, time_spent=2200)

    def test_user___str__(self):
        toString = '''
            username: something
            email: something@gmail.com
            first_name: fname
            last_name: lname
            is_student: True
            is_teacher: False
        '''
        self.assertEqual(self.userObj.__str__(), toString)

    def test_student___str__(self):
        toString = 'student username: something'
        self.assertEqual(self.studentObj.__str__(), toString)
    def test_teacher___str__(self):
        toString = 'teacher username: something'
        self.assertEqual(self.teacherObj.__str__(), toString)
    def test_classroom___str__(self):
        toString = '''
            class_name: class1
            teacher: teacher username: something
        '''
        self.assertEqual(toString, self.classroomObj.__str__())
    def test_Documnt___str__(self):
        toString = 'doc name : doc\ndoc_file: somepath'
        self.assertEqual(toString, self.documentObj.__str__())
    def test_Enrolled_in___str__(self):
        toString = '''
        student: something
        classroom : class1
        status: True
        '''
        self.assertEqual(toString, self.enrolled_in_obj.__str__())
    def test_Student_Document___str__(self):
        toString = '''student: something
        class: class1
        document: doc
        time: 2200'''
        self.assertEqual(toString, self.student_doc_obj.__str__())

