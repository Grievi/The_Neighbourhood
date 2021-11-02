from django.urls import path
from app import views

urlpatterns=[
    path('', views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name= 'signup'),
    path('N_hoods/', views.neighbourhood, name='hood'),
    path('new', views.create_hood, name='create_new'),
    path('move_in/<id>', views.move_in, name='move_in'),
    path('vacate/<id>', views.vacate, name='leave_hood'),
    path('profile/<username>', views.profile, name='profile_edit'),
    path('profile/<username>/edit/', views.edit_profile, name='profile_edit'),
    path('search/', views.business_search, name='search'),
]