from django.shortcuts import get_object_or_404, render,redirect
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


@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile.html',{'username':username})

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit', user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {'form': form})

def business_search(request):
    if request.method == 'GET':
        form = BusinessForm(request.POST)
        if form.is_valid():
            name = request.GET.get("title")
            if name:
                search_results = Business.objects.filter(name__icontains=name).all()
                print(search_results)
                message = f'name'
                params = {
                    'search_results': search_results,
                    'message': message
                } 
                return render(request, 'searchresults.html', params)
            else:
                message = "Something went wrong! Try Again "
    return render(request, "searchresults.html")

@login_required(login_url='login')
def neighbourhood(request):
    neighbourhoods = NeighbourHood.objects.all()
    neighbourhoods = neighbourhoods[::-1]
    params = {
        'neighbourhoods': neighbourhoods,
    }
    return render(request, 'neighbourhoods.html', params)

@login_required(login_url='login')
def create_neighbourhood(request):
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

@login_required(login_url='login')
def vacate(request,id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')

@login_required(login_url='login')
def move_in(request,id):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hood')


def single_hood(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            businessForm = form.save(commit=False)
            businessForm.neighbourhood = hood
            businessForm.user = request.user.profile
            businessForm.save()
            return redirect('single-hood', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'single_hood.html', params)

def hood_members(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'members.html', {'members': members})

def create_post(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('single-hood', hood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

