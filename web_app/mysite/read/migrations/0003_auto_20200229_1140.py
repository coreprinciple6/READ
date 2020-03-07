# Generated by Django 3.0.3 on 2020-02-29 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0002_classroom_document_enrolled_in_student_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_file',
            field=models.FileField(default=None, upload_to='read/documents/'),
        ),
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.ImageField(default=None, upload_to='read/students/'),
        ),
    ]