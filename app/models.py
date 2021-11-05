from django.db import models
from django.contrib.auth.models import User
from datetime import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver

class NeighbourHood(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hood')
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    occupants_count=models.IntegerField(null=True, blank=True)
    description = models.TextField()
    health_tell = models.IntegerField(null=True, blank=True)
    police_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}'
    
    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def search_neighborhood(cls, N_hood_id):
        return cls.objects.filter(id=N_hood_id)

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    location = models.CharField(max_length=50, blank=True, null=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, related_name='hood_member', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
class Post(models.Model):
    
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    N_hood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='hood_post', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Business(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE,related_name='business')
    created_at = models.DateTimeField(auto_now_add=True)

    def create_business(self):
        self.save()

    def __str__(self):
        return self.name

    def delete_business(self):
        self.delete()

    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()


    



    
