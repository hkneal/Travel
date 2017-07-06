from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import UserName, Appointment
from .forms import login_form, register_form, add_appt_form, edit_appt_form
import datetime
# Create your views here.

def getDashboardContext(req):
    user = UserName.objects.get(id=req.session['id'])
    scheduled_appts = Appointment.objects.filter(user=user.id, appt_date=datetime.date.today()).order_by('-appt_time')
    other_appts = Appointment.objects.filter(user=user.id).exclude(appt_date=datetime.date.today())
    context = {
        'appts': scheduled_appts,
        'other_appts' : other_appts,
        'today' : datetime.date.today(),
        'add_appt_form' : add_appt_form()
    }
    return context

def index(req):
    print "In Index"
    context = {
        'login_form' : login_form(),
        'register_form' : register_form()
    }
    return render(req, 'travel_app/index.html', context)

def register(req):
    if req.method == 'POST':
        form = register_form(req.POST)
        if form.is_valid():
            print "Valid Registration"
            postData = {
                'name' : form.cleaned_data['name'],
                'email' : form.cleaned_data['email'],
                'password' : form.cleaned_data['password'],
                'dob' : form.cleaned_data['dob']
                }
            user = UserName.objects.register(postData)
            req.session['id'] = user['user'].id
            req.session['name'] = user['user'].name
            context = getDashboardContext(req)
            return render(req, 'travel_app/dashboard.html', context)
        else:
            context = {
                'login_form' : login_form(),
                'register_form' : form
            }
            return render(req, 'travel_app/index.html', context)
    else:
        return redirect('/')

def login(req):
    if req.method == 'POST':
        form = login_form(req.POST)
        if form.is_valid():
            print "Valid Registration"
            postData = {
                'password' : form.cleaned_data['password'],
                'email' : form.cleaned_data['email']
                }
            user = UserName.objects.login(postData)
            req.session['id'] = user['user'].id
            req.session['name'] = user['user'].name
            context = getDashboardContext(req)
            return render(req, 'travel_app/dashboard.html', context)
        else:
            print "Invalid Registration"
            context = {
                'login_form' : form,
                'register_form' : register_form()
            }
            return render(req, 'travel_app/index.html', context)
    else:
        return redirect('/')

def dashboard(req):
    user = UserName.objects.get(id=req.session['id'])
    scheduled_appts = Appointment.objects.filter(user=user.id, appt_date=datetime.date.today()).order_by('-appt_time')
    other_appts = Appointment.objects.filter(user=user.id).exclude(appt_date=datetime.date.today())
    context = {
        'appts': scheduled_appts,
        'other_appts' : other_appts,
        'today' : datetime.date.today(),
        'add_appt_form' : add_appt_form()
    }
    return render(req, 'travel_app/dashboard.html', context)

def add_appt(req):
    user = UserName.objects.get(id=req.session['id'])
    if req.method == 'POST':
        form = add_appt_form(req.POST)
        if form.is_valid():
            Appointment.objects.create(
                task = form.cleaned_data['task'],
                appt_date = form.cleaned_data['appt_date'],
                appt_time = form.cleaned_data['appt_time'],
                status = "Pending",
                user = user
            )
            context = getDashboardContext(req)
            return render(req, 'travel_app/dashboard.html', context)
        else:
            scheduled_appts = Appointment.objects.filter(user=user.id, appt_date=datetime.date.today()).order_by('-appt_time')
            other_appts = Appointment.objects.filter(user=user.id).exclude(appt_date=datetime.date.today())
            context = {
                'appts': scheduled_appts,
                'other_appts' : other_appts,
                'today' : datetime.date.today(),
                'add_appt_form' : form
            }
            return render(req, 'travel_app/dashboard.html', context)
    else:
        scheduled_appts = Appointment.objects.filter(user=user.id, appt_date=datetime.date.today()).order_by('-appt_time')
        other_appts = Appointment.objects.filter(user=user.id).exclude(appt_date=datetime.date.today())
        context = {
            'appts': scheduled_appts,
            'other_appts' : other_appts,
            'today' : datetime.date.today(),
            'add_appt_form' : add_appt_form()
        }
        return render(req, 'travel_app/dashboard.html', context)

def edit_appt(req, id):
    user = UserName.objects.get(id=req.session['id'])
    appt = Appointment.objects.get(id=id)
    if req.method == 'POST':
        form = edit_appt_form(req.POST)
        if form.is_valid():
            postData = {
                'id' : appt.id,
                'task' : form.cleaned_data['task'],
                'status' : form.cleaned_data['status'],
                'appt_date' : form.cleaned_data['appt_date'],
                'appt_time' : form.cleaned_data['appt_time']
                }
            Appointment.objects.update_info(postData)
            context = getDashboardContext(req)
            return render(req, 'travel_app/dashboard.html', context)
            # return render(req, 'user_app/edit_user.html', context)
        else:
            context = {
                'appt' : appt,
                'edit_appt_form' : form
                }
            return render(req, 'travel_app/edit.html', context)
    else:
        # updateInfo = update_info_form()
        updateInfo =  edit_appt_form(initial={
            'task': appt.task,
            'appt_date': appt.appt_date,
            'status' : appt.status,
            'appt_time': appt.appt_time
            })
        context = {
            'appt' : appt,
            'edit_appt_form' : updateInfo
            }
        return render(req, 'travel_app/edit.html', context)

def delete(req, id):
    appt = Appointment.objects.get(id=id).delete()
    context = getDashboardContext(req)
    return render(req, 'travel_app/dashboard.html', context)

def logout(req):
    del req.session['id']
    del req.session['name']
    return redirect('/')
