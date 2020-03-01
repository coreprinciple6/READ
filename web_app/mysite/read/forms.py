from django import forms
from .models import User, Student, Teacher, Classroom
from django.utils.translation import gettext_lazy


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class LogoutForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput())



class RegistrationForm(forms.ModelForm):
    CHOICES = [('student', 'Student'), ('teacher', 'Teacher')]
    type_of_user = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'password', 'repeat_password', 'email', 'first_name', 'last_name', 'type_of_user']
        labels = {
            'repeat_password' : gettext_lazy('Repeat Password'),
        }
        widgets = {
            'password' : forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeat_password')


        if(password != repeated_password):
            raise forms.ValidationError('Passwords do not match')


class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['start_date', 'end_date', 'teacher']

