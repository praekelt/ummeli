"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.core.urlresolvers import reverse
from ummeli.webservice.utils import APIClient
from django.contrib.auth.models import User
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
        resp = self.client.get('%s?%s' % (reverse('api:getuserdata'),
            urllib.urlencode({
                'username': username
            }))
        )
        
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEquals(len(data), 16)
        user.delete()
        
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
        user.delete()

    def test_get_data_for_invalid_user(self):
        username = 'user'
        password = 'password'
        
        user = User.objects.create(username=username, password=password)
        resp = self.client.get('%s?%s' % (reverse('api:getuserdata'),
            urllib.urlencode({
                'username': 'wronguser'
            }))
        )
        
        print resp.content
        self.assertEquals(resp.status_code, 404)
        user.delete()
