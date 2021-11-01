from django.db import models
from django.contrib.auth.models import User

class NeighbourHood(models.Model):
    admin = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='hood')
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    occupants_count=models.IntegerField(null=True, blank=True)
    description = models.TextField()
    
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=80, blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    location = models.CharField(max_length=50, blank=True, null=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, related_name='hood_member', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def save_profile(self):
        self.save()