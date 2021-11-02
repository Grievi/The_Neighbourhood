from django.test import TestCase
from django.contrib.auth.models import User
from app.models import *

class NeighbourhoodTestClass(TestCase):
    def setUp(self):
        # create an admin user
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.neighbourhood = NeighbourHood(
            name='This is a test', location=self.location, occupants_count=100, admin_id=self.admin.id)

    def test_instance(self):
        self.assertTrue(isinstance(self.neighbourhood, NeighbourHood))

    def test_save_method(self):
        self.neighbourhood.create_neigbourhood()
        neighbourhoods = NeighbourHood.objects.all()
        self.assertTrue(len(neighbourhoods) > 0)

    def test_delete_method(self):
        self.neighbourhood.create_neigborhood()
        self.neighbourhood.delete()
        neighbourhoods = NeighbourHood.objects.all()
        self.assertTrue(len(neighbourhoods) == 0)
