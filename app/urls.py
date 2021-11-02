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
    path('profile/<username>', views.profile, name='profile_edit'),
    # path('profile/<username>/edit/', views.edit_profile, name='profile_edit'),
    path('search/', views.business_search, name='search'),
    path('<hood_id>/members', views.hood_members, name='members'),
    path('<hood_id>/post', views.create_post, name='post'),
    
]