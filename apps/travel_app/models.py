from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
import bcrypt, datetime

class UserManager(models.Manager):
    def register(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
        user = UserName.objects.create(
            name = postData['name'],
            email = postData['email'],
            password = hashed_pw,
            dob = postData['dob']
        )
        return {
            'user':user
            # 'message': "Thank You For Registering!"
            }

    def login(self, postData):
        password = postData['password']
        email = postData['email']
        user = UserName.objects.get(email = postData['email'])
        return {
            'user':user
            # 'message' : "You Have Successfully Logged In!"
            }

class AppointmentManager(models.Manager):
    def update_info(self, postData):
        user = postData['user']
        newDate = postData['appt_date']
        newTime = postData['appt_time']
        appt_list = user.appts_scheduled.all()
        for appt in appt_list:
            if appt.appt_date == newDate and appt.appt_time == newTime:
                return { 'error' : 'You already have an appointment for this Date and Time!'}
        appt = Appointment.objects.filter(id=postData['id']).update(
            task = postData['task'],
            status = postData['status'],
            appt_date = newDate,
            appt_time = newTime
        )
        return {
            'appt' : appt
        }

    def add_appt(self, postData):
        user = postData['user']
        newDate = postData['appt_date']
        newTime = postData['appt_time']
        appt_list = user.appts_scheduled.all()
        for appt in appt_list:
            if appt.appt_date == newDate and appt.appt_time == newTime:
                return { 'error' : 'You already have an appointment for this Date and Time!'}
        appt = Appointment.objects.create(
            task = postData['task'],
            status = postData['status'],
            appt_date = newDate,
            appt_time = newTime,
            user = user
        )
        return {
            'appt' : appt
        }

# Create your models here.
class UserName(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    dob = models.DateField()
    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=200)
    appt_date = models.DateField()
    appt_time = models.TimeField()
    status = models.CharField(max_length=7, null=False)
    user = models.ForeignKey(UserName, related_name="appts_scheduled")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AppointmentManager()
