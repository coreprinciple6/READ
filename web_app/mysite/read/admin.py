from django.contrib import admin

from .models import User, Student, Teacher, Classroom, Document, Student_Document, Enrolled_in
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Document)
admin.site.register(Student_Document)
admin.site.register(Enrolled_in)

