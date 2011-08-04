"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.test import TestCase
from django.core.urlresolvers import reverse
from ummeli.webservice.utils import APIClient
from ummeli.webservice.models import UserProfile, Curriculumvitae
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
        
        user = User.objects.create(username=username, password=password)
        resp = self.client.get('%s?%s' % (reverse('api:getuserdata'),
            urllib.urlencode({
                'username': username
            }))
        )
        
        print resp.content
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEquals(len(data), 1)
        
    def test_get_data_for_user_with_no_profile(self):
        username = 'user'
        password = 'password'
        
        user = User.objects.create(username=username, password=password)
        resp = self.client.get('%s?%s' % (reverse('api:getuserdata'),
            urllib.urlencode({
                'username': username
            }))
        )
        
        print resp.content
        self.assertIsNotNone(user.get_profile())
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEquals(len(data), 1)
        
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
        data = json.loads(resp.content)
        self.assertEquals(len(data), 1)
