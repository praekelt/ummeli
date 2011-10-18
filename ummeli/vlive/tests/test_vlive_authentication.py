from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import urllib

class VliveAuthenticationTestCase(TestCase):
    
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
        resp = self.client.get(reverse('index'))
         #  there shouldn't be a Location header as this would mean a redirect
         #  to a login URL
        self.assertEquals(resp.get('Location', None), None)
        self.assertEquals(resp.status_code, 200)
        
    def test_login_view(self):
        msisdn = '0123456789'
        password = 'password'
        user = User.objects.create_user(msisdn, '%s@domain.com' % msisdn, 
                                        password)
        resp = self.client.get(reverse('login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': password, 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        self.assertEquals(resp.status_code, 200)  # redirect to index
        self.assertContains(resp, 'Edit CV')
        
        resp = self.client.get(reverse('login'), 
                               {'password': 'wrong_pin', '_action': 'POST'},
                                HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        self.assertEquals(resp.status_code, 200)      
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('index'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        #self.assertEquals(resp.status_code, 302)  # redirect to login
        #self.assertEquals(resp.get('Location', None), 
        #                'http://testserver/vlive/login?next=/vlive/')
        
        resp = self.client.get(reverse('login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Click here to create profile.')
        
        resp = self.client.get(reverse('register'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Create pin for %s' % (msisdn))
        
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password, 
                                'password2': password,  '_action': 'POST'},  
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'You are now registerd.')
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': password, 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Edit CV')

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('register'), 
                               {'username': msisdn, 'password1': password, 
                               'password2': 'wrong',  '_action': 'POST'}, 
                               HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertContains(resp, 'Pin codes don&apos;t match.')
        
    def test_forgot_pin(self):
        msisdn = '0123456789'
        password = 'password'
        
        #register user
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password, 
                                'password2': password,  '_action': 'POST'},  
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        resp = self.client.get(reverse('forgot'), HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertContains(resp, 'Pin will be sent to %s.' % msisdn)
        
        resp = self.client.get(reverse('forgot'), {'_action': 'POST'}, 
                               HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertContains(resp, 'Your new pin has been sent')
        
    def test_change_pin(self):
        msisdn = '0123456789'
        password = 'password'
        
        #register user
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password, 
                                'password2': password,  '_action': 'POST'},  
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        resp = self.client.get(reverse('login'), 
                    {'username': msisdn, 'password': password, '_action': 'POST'}, 
                    HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        resp = self.client.get(reverse('password_change'), 
                               HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        
        self.assertContains(resp, 'Change pin for %s' % msisdn)
        
        resp = self.client.get(reverse('password_change'), 
                               {'_action': 'POST',  'old_password': password, 
                               'new_password1': '1234',  'new_password2': '1234'}, 
                               HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertContains(resp, 'Your pin has been changed')
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': '1234', 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        self.assertContains(resp, 'Edit CV')
