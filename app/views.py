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
            return redirect('hood')

        else:
            messages.success(request,"Oops Something went wrong, please Login!")

            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html', {"message": message})

def user_logout(request):
    logout(request)
    messages.success(request, ("You have logged out"))
    return redirect('login')

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

            return redirect('login')
            
    else:
        form=UserCreationForm()
    return render(request, 'registration/signup.html', {"message": message,"form": form})


@login_required(login_url='login')
def profile(request):
    
    current_user = request.user
    profile = Profile.objects.filter(
        user_id=current_user.id).first()
    posts = Post.objects.filter(user_id=current_user.id)
    neighbourhood = NeighbourHood.objects.all()
    businesses = Business.objects.filter(user_id=current_user.id)
    businesses = Business.objects.filter(user_id=current_user.id)
    return render(request, 'profile/profile.html', {'profile': profile,'posts':posts,'neighbourhood':neighbourhood,'businesses':businesses})

@login_required(login_url='login')
def edit_profile(request):
    if request.method =='POST':
        current_user=request.user
        name = request.POST['name']
        location = request.POST['location']
        neighbourhood=request.POST['neighbourhood']

        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = NeighbourHood.objects.get(name=neighbourhood)

        profile_picture = request.FILES['profile_picture']
        profile_url=profile_picture['url']

        user =User.objects.get(id=current_user.id)

        if Profile.objects.filter(user_id=current_user.id).exists():
            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_picture =profile_url
            profile.neighbourhood = neighbourhood
            profile.save()
        else:
            profile = Profile(
                user_id=current_user.id,
                name=name,
                profile_picture=profile_url,
                neighbourhood=neighbourhood,
                location=location
            )

            profile.save_profile()

        user.name=name
        user.save()

        return redirect('profile/profile', {"success": "Profile Updated Successfully"})
    else:
        return render(request, 'profile.html', {'danger':'Profile update Failed!'})
        


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
def create_post(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return redirect('hood')
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})


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


def hood_members(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'members.html', {'members': members})

# def single_hood(request, hood_id):
#     hood = NeighbourHood.objects.get(id=hood_id)
#     business = Business.objects.filter(neighbourhood=hood)
#     posts = Post.objects.filter(hood=hood)
#     posts = posts[::-1]
#     if request.method == 'POST':
#         form = BusinessForm(request.POST)
#         if form.is_valid():
#             b_form = form.save(commit=False)
#             b_form.neighbourhood = hood
#             b_form.user = request.user.profile
#             b_form.save()
#             return redirect('single-hood', hood.id)
#     else:
#         form = BusinessForm()
#     params = {
#         'hood': hood,
#         'business': business,
#         'form': form,
#         'posts': posts
#     }
#     return render(request, 'singlehood.html', params)

