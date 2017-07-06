from django import forms
from .models import UserName, Appointment
from django.core.exceptions import ValidationError
import bcrypt, datetime, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def validateName(strInput):
    if not strInput.replace(' ','').isalpha():
        return False
    if len(strInput) < 3:
        return False
    return True

def hasNumbers(strInput):
    return any(char.isdigit() for char in strInput)

def hasUpper(strInput):
    return any(char.isupper() for char in strInput)

STATUS_CHOICES = [
    ('Done', 'Done'),
    ('Pending', 'Pending'),
    ('Missed', 'Missed'),
    ]

class DateInput(forms.DateInput):
    input_type = 'date'

class login_form(forms.Form):
    email = forms.EmailField(label='Email:', max_length=45, min_length=7, required=True, widget=forms.EmailInput)
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_email(self):
        thisEmail = self.cleaned_data['email']
        if not UserName.objects.filter(email=thisEmail).exists():
            raise ValidationError('You must first register!')
        return thisEmail

    def clean_password(self):
        form_data = self.cleaned_data
        password = self.cleaned_data['password']
        email = form_data.get('email')
        try:
            user = UserName.objects.get(email = email)
        except:
            raise ValidationError('You Must Register First!')
        hashed_pw = user.password
        if bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), hashed_pw.encode(encoding="utf-8", errors="strict")) != hashed_pw:
            raise ValidationError('Incorrect password!')
        return password

class register_form(forms.Form):
    email = forms.EmailField(label='Email:', max_length=45, min_length=7, required=True, widget=forms.EmailInput)
    name = forms.CharField(label='Name:', max_length=45, min_length=3, required=True)
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)
    dob = forms.DateField(label='Date of Birth:', widget=forms.TextInput(attrs={'id' : 'datepicker'}),required=True, initial='   /   /   ')

    def clean_email(self):
        thisEmail = self.cleaned_data['email']
        if UserName.objects.filter(email=thisEmail).exists():
            raise ValidationError('Email already exists!')
        elif not EMAIL_REGEX.match(thisEmail):
            raise ValidationError('Please enter a valid email address')
        return thisEmail

    def clean_name(self):
        name = self.cleaned_data['name']
        if not validateName(name):
            raise ValidationError('Your name should be greater than 2 characters and less than 45 characters and should not contain numbers or symbols')
        return name

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Passwords must contain as least 8 characters/numbers')
        elif not hasNumbers(password):
            raise ValidationError('Password should contain at least 1 number!')
        elif not hasUpper(password):
            raise ValidationError('Passwords require at least 1 uppercase letter!')
        return password

    def clean_confirm_password(self):
        form_data = self.cleaned_data
        password = form_data.get('password')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Password and Confirm Password must match')
        return confirm_password

    def clean_dob(self):
        birthDate = self.cleaned_data['dob']
        if birthDate >= datetime.date.today():
            raise ValidationError('Birth Date Must be Before Today!')
        return birthDate

class add_appt_form(forms.Form):
    appt_date = forms.DateField(label='Date:', required=True, widget=forms.TextInput(attrs={'id' : 'datepicker'}))
    appt_time = forms.TimeField(label='Time (eg 13:00 for 1:00 pm):', initial='00:00', widget=forms.TimeInput(format='%H:%M %p'), required=True)
    task = forms.CharField(label='Tasks:', max_length=200, min_length=3, required=True)

    def clean_appt_date(self):
        apptDate = self.cleaned_data['appt_date']
        if apptDate < datetime.date.today():
            raise ValidationError('Appointment Date Must be Today or After!')
        return apptDate

    def clean_task(self):
        tasks = self.cleaned_data['task']
        if len(tasks) < 3:
            raise ValidationError('Task must be at least 3 characters')
        return tasks

class edit_appt_form(forms.Form):
    task = forms.CharField(label='Tasks:', max_length=200, min_length=3, required=True)
    status = forms.ChoiceField(choices=(STATUS_CHOICES))
    appt_date = forms.DateField(label='Date:', required=True, widget=forms.TextInput(attrs={'id' : 'datepicker'}))
    appt_time = forms.TimeField(label='Time (eg 13:00 for 1:00 pm):', initial='00:00', widget=forms.TimeInput(format='%H:%M'), required=True)

    def clean_appt_date(self):
        apptDate = self.cleaned_data['appt_date']
        if apptDate < datetime.date.today():
            raise ValidationError('Appointment Date Must be Today or After!')
        return apptDate

    def clean_task(self):
        tasks = self.cleaned_data['task']
        if len(tasks) < 3:
            raise ValidationError('Task must be at least 3 characters')
        return tasks
