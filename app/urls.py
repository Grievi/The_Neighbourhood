from django.urls import path
from app import views

urlpatterns=[
    path('', views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name= 'signup'),
    path('N_hoods/', views.neighbourhood, name='hood'),
    path('new', )
]