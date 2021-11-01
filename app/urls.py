from django.urls import path
from app import views

urlpatterns=[
    path('', views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name= 'signup'),
]