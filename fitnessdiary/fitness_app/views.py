from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import bcrypt

def index(request):
    return render(request, 'login.html')

def signin(request):
    return render(request, 'login.html')

def register_form(request):
    return render(request, 'registration.html')

def edit_account(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, "edit_account.html", context)

def dashboard(request):
    if 'user_id' not in request.session: #validate user is logged in
        return redirect('/')
    user = User.objects.get(id=request.session['user_id']) #will pass id belong to the user
    context = {
        'user' : user
    }
    return render (request, 'dashboard.html', context)

def back(request):
    if 'user_id' not in request.session: #validate user is logged in
        return redirect('/')
    return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

def createroutine(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id']) #will pass id belong to the user
    context = {
        'user' : user
    }
    return render(request, 'create_routine.html', context)

def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST) #to validate the form is completed correctly
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        this_user = User.objects.get(user_name=request.POST['user_name'])
        request.session['user_user_name'] = this_user.user_name
        request.session['user_first_name'] = this_user.first_name
        request.session['user_last_name'] = this_user.last_name
        request.session['user_email'] = this_user.email
        request.session['user_id'] = this_user.id
        return redirect('/dashboard')
    return render(request, "dashboard.html") 

def registration(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST) #to validate the form is completed correctly
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/register')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() #to hash the password
        new_user = User.objects.create ( #to create a new user
            user_name = request.POST['user_name'],
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_user_name'] = new_user.user_name
        request.session['user_first_name'] = new_user.first_name
        request.session['user_last_name'] = new_user.last_name
        request.session['user_email'] = new_user.email
        request.session['user_id'] = new_user.id
        send_mail('Welcome to Fitness Diary', 
        f'Hello {new_user.first_name}! Thank you for joining us and hope you enjoy this app as much as we did developing', 
        settings.EMAIL_HOST_USER, 
        [new_user.email], 
        fail_silently=False)
        return redirect ('/dashboard')
    return redirect ('/')

def delete_account(request):
    if 'user_id' not in request.session:
        return redirect('/')   
    user = User.objects.get(id=request.session['user_id'])
    user.delete()
    return redirect('/')

def update_account(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/edit_account')