from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

import urllib

class VliveAuthenticationTestCase(TestCase):

    def setUp(self):
        self.msisdn = '0123456789'
        self.pin = '1234'
        self.client = Client(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)

    def tearDown(self):
        pass

    def test_index_page(self):
        self.client.login(username=self.msisdn, password=self.pin)
        resp = self.client.get(reverse('index'))
         #  there shouldn't be a Location header as this would mean a redirect
         #  to a login URL
        self.assertEquals(resp.get('Location', None), None)
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.get(reverse('login'), )
        self.assertEquals(resp.status_code, 200)

        resp = self.client.get(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
            '_action': 'POST',
        })

        self.assertEquals(resp.status_code, 200)  # redirect to index
        self.assertContains(resp, 'You have been logged in')

        resp = self.client.get(reverse('login'),{
            'password': 'wrong_pin',
            '_action': 'POST',
        })

        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):

        resp = self.client.get(reverse('login'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Enter Pin to sign in.')
        self.assertContains(resp, 'Forgotten your Pin?')

        resp = self.client.get(reverse('register'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Create pin for %s' % (self.msisdn))

        resp = self.client.get(reverse('register'), {
            'new_password1': self.pin,
            'new_password2': self.pin,
            '_action': 'POST'
        })

        print resp.content
        user = ModelBackend().authenticate(username=self.msisdn, password=self.pin)
        self.assertTrue(user)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'You are now registered.')

        #test automatic login
        resp = self.client.get(reverse('edit'))
        self.assertContains(resp, 'Personal')

        resp = self.client.get(reverse('logout'))
        self.assertContains(resp,  'You have been logged out')

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'

        resp = self.client.get(reverse('register'),
                               {'username': msisdn, 'password1': password,
                               'password2': 'wrong',  '_action': 'POST'})
        self.assertContains(resp, 'Pin codes don&apos;t match.')

    def test_forgot_pin(self):
        msisdn = '0123456789'
        password = 'password'

        #register user
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password,
                                'password2': password,  '_action': 'POST'})

        resp = self.client.get(reverse('forgot'))
        self.assertContains(resp, 'Pin will be sent to %s.' % msisdn)

        resp = self.client.get(reverse('forgot'), {'_action': 'POST'})
        self.assertContains(resp, 'Your new pin has been sent')

    def test_change_pin(self):
        msisdn = '0123456789'
        password = 'password'

        #register user
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password,
                                'password2': password,  '_action': 'POST'})

        resp = self.client.get(reverse('login'),
                    {'username': msisdn, 'password': password, '_action': 'POST'})

        resp = self.client.get(reverse('password_change'))

        self.assertContains(resp, 'Change pin for %s' % msisdn)

        resp = self.client.get(reverse('password_change'),
                               {'_action': 'POST',  'old_password': password,
                               'new_password1': '1234',  'new_password2': '1234'})
        self.assertContains(resp, 'Your pin has been changed')

        resp = self.client.get(reverse('login'),
                                {'username': msisdn, 'password': '1234',
                                '_action': 'POST'})

        self.assertContains(resp, 'You have been logged in')
