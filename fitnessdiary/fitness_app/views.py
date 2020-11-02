from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'login.html')

def signin(request):
    return render(request, 'login.html')

def register_form(request):
    return render(request, 'registration.html')

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

def dashboard(request):
    if 'user_id' not in request.session: #validate user is logged in
        return redirect('/')
    user = User.objects.get(id=request.session['user_id']) #will pass id belong to the user
    context = {
        'user' : user
    }
    return render (request, 'dashboard.html', context)

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
        request.session['user_first_name'] = new_user.first_name
        request.session['user_last_name'] = new_user.last_name
        request.session['user_email'] = new_user.email
        request.session['user_id'] = new_user.id
        return redirect ('/dashboard')
    return redirect ('/')