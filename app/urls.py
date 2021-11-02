from django.urls import path
from app import views

urlpatterns=[
   
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name= 'signup'),
    path('', views.neighbourhood, name='hood'),
    path('new', views.create_neighbourhood, name='create_new'),
    path('move_in/<id>', views.move_in, name='move_in'),
    path('vacate/<id>', views.vacate, name='vacate'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.business_search, name='search'),
    path('members/', views.hood_members, name='members'),
    path('post/', views.create_post, name='post'),
    path('profile/', views.edit_profile, name='edit-profile'),
    
]