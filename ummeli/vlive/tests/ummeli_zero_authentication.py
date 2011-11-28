from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
import urllib
import os

class UmmeliZeroAuthenticationTestCase(VLiveTestCase):

    def setUp(self):
        self.msisdn = '012340000'
        self.pin = '1234'
        self.client = Client()
        
        settings.ROOT_URLCONF = 'mobi_urls'
        settings.TEMPLATE_DIRS = ("vlive/templates/0", )
        settings.AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
        settings.MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'vlive.auth.middleware.VodafoneLiveUserMiddleware',
            'vlive.auth.middleware.VodafoneLiveInfoMiddleware',
            'vlive.middleware.FormActionMiddleware',
            'vlive.middleware.AddMessageToResponseMiddleware', 
        )

    def tearDown(self):
        settings.ROOT_URLCONF = 'pml_urls'
        settings.TEMPLATE_DIRS = ("vlive/templates/pml", )
        settings.AUTHENTICATION_BACKENDS = (
        'ummeli.vlive.auth.backends.VodafoneLiveUserBackend',
        'django.contrib.auth.backends.ModelBackend', )
        settings.MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'vlive.auth.middleware.VodafoneLiveUserMiddleware',
            'vlive.auth.middleware.VodafoneLiveInfoMiddleware',
            'vlive.middleware.FormActionMiddleware',
            'vlive.middleware.AddMessageToResponseMiddleware', 
            'vlive.middleware.ModifyPMLResponseMiddleware',
        )

    def test_index_page(self):
        self.client.login(username=self.msisdn, password=self.pin)
        resp = self.client.get(reverse('index'))
         #  there shouldn't be a Location header as this would mean a redirect
         #  to a login URL
        self.assertFalse(resp.get('Location', None))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.post(reverse('register'), {
            'username': self.msisdn,
            'password1': self.pin,
            'password2': self.pin,
        })
        self.assertEquals(resp.status_code, 302)

        resp = self.client.get(reverse('logout'))
        self.assertEquals(resp.status_code, 302)

        resp = self.client.get(reverse('login'), )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Sign in')

        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
        })

        self.assertEquals(resp.status_code, 302)  # redirect to index

        resp = self.client.post(reverse('login'),{
            'password': 'wrong_pin',
        })

        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):

        resp = self.client.get(reverse('login'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Sign in')
        self.assertContains(resp, 'Forgot your PIN?')

        resp = self.client.get(reverse('register'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Sign Up')

        resp = self.client.post(reverse('register'), {
            'username': self.msisdn,
            'password1': self.pin,
            'password2': self.pin,
        })
        
        # check that the PIN has been set and that we can now authenticate
        # with the ModelBackend using the msisdn and pin
        user = ModelBackend().authenticate(username=self.msisdn, password=self.pin)
        
        self.assertEqual(user.username, self.msisdn)
        self.assertEquals(resp.status_code, 302)
        # ensure the session's pin has been set
        self.assertTrue(self.client.session[settings.UMMELI_PIN_SESSION_KEY])

        #test automatic login
        resp = self.client.get(reverse('edit'))
        self.assertContains(resp, 'Personal')

        resp = self.client.get(reverse('logout'))
        self.assertEquals(resp.status_code, 302)
        # ensure the session's pin has been cleared
        self.assertNotIn(settings.UMMELI_PIN_SESSION_KEY, self.client.session)

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'

        resp = self.client.post(reverse('register'), {
            'username': msisdn,
            'password1': password,
            'password2': 'wrong',
        })
        
        self.assertContains(resp, 'The two password fields didn&#39;t match')

    def test_forgot_pin(self):

        #register user
        resp = self.client.post(reverse('register'),{
            'username': self.msisdn,
            'password1': self.pin,
            'password2': self.pin,
        })

        resp = self.client.get(reverse('forgot'))
        self.assertContains(resp, 'Forgot your PIN')

        resp = self.client.post(reverse('forgot'),  {'username':self.msisdn})
        self.assertEquals(resp.status_code, 302)

    def test_change_pin(self):
        # register user
        resp = self.client.post(reverse('register'), {
            'username': self.msisdn,
            'password1': self.pin,
            'password2': self.pin,
        })
        print resp
        self.assertEquals(resp.status_code, 302)
        
        # authorize with pin
        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
        })

        resp = self.client.get(reverse('password_change'))
        # print resp
        self.assertContains(resp, 'Change PIN for %s' % self.msisdn)

        resp = self.client.post(reverse('password_change'),{
            'old_password': self.pin,
           'new_password1': '5678',
           'new_password2': '5678',
        })
        self.assertEquals(resp.status_code, 302)

        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': '5678',
        })

        self.assertEquals(resp.status_code, 302)
