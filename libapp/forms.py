from django import forms
from .models import *

class BookRequestForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), widget=forms.HiddenInput())
    start_date = forms.DateField()
    duration = forms.IntegerField()
    end_date = forms.DateField()

# forms.py

from django import forms
from .models import Book

class BookFilterForm(forms.Form):
    DEPARTMENT_CHOICES = [
        ('', 'All Departments'),
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('MECH', 'MECH'),
        ('IT', 'IT'),
    ]

    SUBJECT_CHOICES = {
        'CSE': [
            ('Subject 1', 'Subject 1'),
            ('Subject 2', 'Subject 2'),
            ('Subject 3', 'Subject 3'),
            ('Subject 4', 'Subject 4'),
            ('Subject 5', 'Subject 5'),
        ],
        'ECE': [
            ('Digital Electronics', 'Digital Electronics'),
            ('Network Theory', 'Network Theory'),
            ('Computer Organization', 'Computer Organization'),
            ('Analog Communication', 'Analog Communication'),
            ('Digital Signal Processing', 'Digital Signal Processing'),
        ],
        'IT' :[
            ('Computer Graphics', 'Computer Graphics'),
            ('Java Programming', 'Java Programming'),
            ('Computer Networks', 'Computer Networks'),
            ('Operating Systems', 'Operating Systems'),
            ('Human Computer Interaction', 'Human Computer Interaction'),
        ],
        'MECH':[
            ('Engineering Drawing', 'Engineering Drawing'),
            ('Material Science', 'Material Science'),
            ('Fluid Mechanics', 'Fluid Mechanics'),
            ('Applied Mechanics', 'Applied Mechanics'),
            ('Automobile Engineering', 'Automobile Engineering'),
        ],
        # Add other departments and their corresponding subjects as needed
    }

    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False)
    subjects = forms.MultipleChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.data:
            department = self.data['department']
            if department:
                self.fields['subjects'].choices = self.SUBJECT_CHOICES.get(department, [])
            else:
                self.fields['subjects'].choices = []
        else:
            self.fields['subjects'].choices = []


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    username = forms.CharField(max_length=50)
    phone = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password','email','phone')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)