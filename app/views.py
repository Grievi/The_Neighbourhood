from django.shortcuts import render
from app.models import *
from django.contrib.auth.models import User


def index(request):
    return render (request, 'index.html')