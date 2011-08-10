"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.core.urlresolvers import reverse
from ummeli.api.utils import APIClient
from django.contrib.auth.models import User

from ummeli.api.models import Curriculumvitae

import json
import urllib

class ApiTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def tearDown(self):
        pass
        
    def test_get_data(self):
        username = 'user'
        password = 'password'
        user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': username
            }))
        )
        
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEquals(len(data), 17)
        
    def test_user_profile_creation(self):
        username = 'user'
        password = 'password'
        
        user = User.objects.create(username=username, password=password, 
            first_name='name', last_name='surname', email='test@test.com')
        
        profile = user.get_profile()
        self.assertEquals(profile.Firstname, 'name')
        self.assertEquals(profile.Surname, 'surname')
        self.assertEquals(profile.Email, 'test@test.com')
        
        user.first_name = 'something'
        user.last_name = 'else'
        user.save()
        profile = user.get_profile()
        self.assertEquals(profile.Firstname, 'something')
        self.assertEquals(profile.Surname, 'else')

    def test_get_data_for_invalid_user(self):
        username = 'user'
        password = 'password'
        
        user = User.objects.create(username=username, password=password)
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': 'wronguser'
            }))
        )
        
        print resp.content
        self.assertEquals(resp.status_code, 404)
    
    def test_registration(self):
        username = 'user'
        password = 'password'

        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        data = json.loads(resp.content)
        self.assertEquals(len(data), 17)
        
        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        self.assertEquals(resp.status_code, 409)
        
    def test_cv_updating(self):
        username = 'user'
        password = 'password'

        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        cv = {
                "TelephoneNumber": '0123456789', 
                "School": None, 
                "Surname": "surname", 
                "HighestGrade": None, 
                "Firstname": "name", 
                "Gender": 'male', 
                "workExperiences": [], 
                "languages": [], 
                "DateOfBirth": None, 
                "references": [], 
                "Location": None, 
                "certificates": [], 
                "HighestGradeYear": 0, 
                "HouseNumber": None, 
                "Email": "an@email.com", 
                "StreetName": None,
                "id": 1,
                "user": User.objects.get(username = username).pk
            }
        resp = self.client.put(reverse('api:userdata'),cv)
        
        self.assertEquals(resp.status_code, 200)
        
        cv = {
                "TelephoneNumber": '0123456789', 
                "School": 'Some school', 
                "Surname": "surname", 
                "HighestGrade": '12', 
                "Firstname": "name", 
                "Gender": 'male', 
                "workExperiences": [], 
                "languages": [], 
                "DateOfBirth": None, 
                "references": [], 
                "Location": None, 
                "certificates": [], 
                "HighestGradeYear": 0, 
                "HouseNumber": None, 
                "Email": "an@email.com", 
                "StreetName": None,
                "id": 1,
                "user": User.objects.get(username = username).pk
            }
        resp = self.client.put(reverse('api:userdata'),cv)
        
        self.assertEquals(resp.status_code, 200)
        
        cv = User.objects.get(username = username).get_profile()
        self.assertEquals(cv.School,'Some school')
        self.assertEquals(cv.HighestGrade,'12')