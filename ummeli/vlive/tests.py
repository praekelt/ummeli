from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import json
import urllib

class VliveTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def tearDown(self):
        pass
        
    def test_index_page(self):
        username = 'user'
        password = 'password'
        user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse('vlive:index'))
        # there shouldn't be a Location header as this would mean a redirect
        # to a login URL
        self.assertEquals(resp.get('Location', None), None)
        self.assertEquals(resp.status_code, 200)
        
    def test_login_view(self):
        msisdn = '0123456789'
        password = 'password'
        user = User.objects.create_user(msisdn, '%s@domain.com' % msisdn, 
                                        password)
        resp = self.client.get(reverse('vlive:login'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.post(reverse('vlive:login'), 
                                {'username': msisdn, 'password': password})
        self.assertEquals(resp.status_code, 302)
        self.assertEquals(resp.get('Location', None), 'http://testserver/vlive')
        
        resp = self.client.post(reverse('vlive:login'), 
                                {'username': 'unknown', 'password': password})
        self.assertEquals(resp.status_code, 200)        
        self.assertContains(resp, 'Sign in failed')