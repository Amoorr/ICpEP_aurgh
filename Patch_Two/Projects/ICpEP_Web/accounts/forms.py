"""
forms.py is responsible for handling the user input. It receives the input of the user, validates them,
and secures them before putting these data to the database
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm # Using default form maker
from .models import CustomUser # Using the custom user model
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")
    acad_year = forms.IntegerField(required=False, label="Academic Year")
    acad_block = forms.CharField(max_length=1, required=False, label="Academic Block")
    membership_id = forms.CharField(max_length=20, required=False, label="Membership ID")
    student_id = forms.CharField(max_length=10, required=False, label="Student ID")

    class Meta:
        model = CustomUser
        fields = [
            'given_name', 'last_name', 'email', 'password1', 'password2',
            'role', 'acad_year', 'acad_block', 'membership_id', 'student_id'
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        # Validate student-specific fields only if role is student
        if role == 'student':
            acad_year = cleaned_data.get('acad_year')
            acad_block = cleaned_data.get('acad_block')
            membership_id = cleaned_data.get('membership_id')
            student_id = cleaned_data.get('student_id')

            if not all([acad_year, acad_block, membership_id, student_id]):
                raise forms.ValidationError("All student fields are required for the 'student' role.")

        return cleaned_data



class LoginForm(forms.Form):
    """
    This is the form presented when the user wants to log in
    """
    username = forms.CharField(max_length=150, label='Email')  # Use email as the username
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password.')

        return cleaned_data
    
class AdminEditAccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['membership_id', 'acad_year', 'acad_block']
        widgets = {
            'membership_id': forms.TextInput(attrs={'class': 'form-control'}),
            'acad_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'acad_block': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 1}),
        }


