from django.shortcuts import render,redirect
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import login,authenticate,logout


def index(request):
    return render (request, 'index.html')

def user_login(request):
    message = 'Login to Proceed'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,f"Welcome {username} to Movie Gallore!")
            return redirect('home')

        else:
            messages.success(request,"Oops Somethinge went wrong, please Login!")

            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html', {"message": message})

def user_logout(request):

    logout(request)
    messages.success(request, ("You have logged out"))
    return redirect('index')

def user_signup(request):
    message='Create an account here!'
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user= authenticate(username=username, password=password)
            # login(request, user)
            messages.success(request,("Account created successfully"))

            return redirect('index')
            
    else:
        form=UserCreationForm()
    return render(request, 'registration/signup.html', {"message": message,"form": form})