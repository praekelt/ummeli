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
        resp = self.client.get(reverse('vlive:login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.post(reverse('vlive:login'), 
                                {'username': msisdn, 'password': password})
                                
        self.assertEquals(resp.status_code, 302) #redirect to index
        self.assertEquals(resp.get('Location', None), 'http://testserver/vlive')
        
        resp = self.client.post(reverse('vlive:login'), {'password': 'wrong_pin'},
                                HTTP_X_UP_CALLING_LINE_ID=msisdn)
                                
        self.assertEquals(resp.status_code, 200)        
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('vlive:index'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 302) #redirect to login
        self.assertEquals(resp.get('Location', None), 
                        'http://testserver/vlive/login?next=/vlive/')
        
        resp = self.client.get(reverse('vlive:login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Click here to create profile.')
        
        resp = self.client.get(reverse('vlive:register'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Create pin for %s' % (msisdn))
        
        resp = self.client.post(reverse('vlive:register'), 
                                {'username': msisdn, 'password1': password, 
                                'password2': password})
        self.assertEquals(resp.status_code, 302) #redirect to index
        self.assertEquals(resp.get('Location', None), 'http://testserver/vlive/')
        
        resp = self.client.post(reverse('vlive:login'), 
                                {'username': msisdn, 'password': password})
        self.assertEquals(resp.status_code, 302) #redirect to index
        self.assertEquals(resp.get('Location', None), 'http://testserver/vlive')

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.post(reverse('vlive:register'), 
                                {'username': msisdn, 'password1': password, 
                                'password2': 'wrong'})
        print resp
        self.assertContains(resp, 'Pin codes don&apos;t match.')
        

class VliveCVTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        username = 'user'
        password = 'password'
        self.user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
    
    def tearDown(self):
        pass
        
    def test_edit_personal_page(self):
        resp = self.client.get(reverse('vlive:edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('vlive:edit'), 
                                        'personal'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'firstName': 'Milton', 'gender': 'Male'}
        resp = self.client.post('%s/%s' % (reverse('vlive:edit'), 
                                        'personal'), post_data)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.firstName, 'Milton')
        self.assertEquals(cv.gender, 'Male')
        
        post_data = {'cancel': 'True'}
        resp = self.client.post('%s/%s' % (reverse('vlive:edit'), 
                                        'personal'), post_data)
        self.assertEquals(resp.status_code, 302) #redirect to edit menu
        self.assertEquals(resp.get('Location', None), 'http://testserver/vlive/edit')