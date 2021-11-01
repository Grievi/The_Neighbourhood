from django import forms
from django.contrib.auth.models import User
from app.models import Profile

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'neighbourhood')

