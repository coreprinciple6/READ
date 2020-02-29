from django import forms
from .models import User, Student, Teacher


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class LogoutForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput())



class RegistrationForm(forms.ModelForm):
    CHOICES = [('student', 'Student'), ('teacher', 'Teacher')]
    type_of_user = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'type_of_user')
