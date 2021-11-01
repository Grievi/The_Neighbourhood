from django.db import models

class NeighbourHood(models.Model):
    admin = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='hood')
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    occupants=models.IntegerField(null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return f'{self.name}'
    
    def create_neighborhood(self):
        self.save()