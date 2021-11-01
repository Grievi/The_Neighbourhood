from django.shortcuts import render,redirect
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from app.forms import *

@login_required(login_url='login')
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
            messages.success(request,f"Welcome {username} to Th Neighbourhood!")
            return redirect('index')

        else:
            messages.success(request,"Oops Something went wrong, please Login!")

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
            login(request, user)
            messages.success(request,("Account created successfully"))

            return redirect('index')
            
    else:
        form=UserCreationForm()
    return render(request, 'registration/signup.html', {"message": message,"form": form})

def neighbourhood(request):
    neighbourhoods = NeighbourHood.objects.all()
    neighbourhoods = neighbourhoods[::-1]
    params = {
        'neighbourhoods': neighbourhoods,
    }
    return render(request, 'neighbourhoods.html', params)

def create_hood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hood')
    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})

def profile(request, username):
    return render(request, 'profile.html',username)

def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'editprofile.html', {'form': form})