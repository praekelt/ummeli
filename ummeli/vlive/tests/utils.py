from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ummeli.base.models import Language

class VLiveClient(Client):
    def post(self, url, data={}, **kwargs):
        defaults = {
            '_action': 'POST',
        }
        defaults.update(data)
        return super(VLiveClient, self).get(url, defaults, **kwargs)

class VLiveTestCase(TestCase):
    def get_user(self, msisdn=None):
        if not msisdn:
            msisdn = self.msisdn
        return User.objects.get(username=msisdn)

    def register(self, msisdn = None):
        if not msisdn:
            msisdn = self.msisdn
            
        resp = self.client.post(reverse('register'), {
            'username': msisdn,
            'new_password1': self.pin,
            'new_password2': self.pin,
        })
        self.assertContains(resp, 'Submitted successfully.')
        return resp

    def login(self):
        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
        })
        self.assertNotContains(resp, 'Sign in failed.')
        return resp

    def logout(self):
        return self.client.get(reverse('logout'))

    def assertVLiveRedirects(self, resp, url, text=None):
        if not text:
            text = 'Please wait while we automatically redirect you.'
        timer_html = '<TIMER href="%s' % url
        self.assertContains(resp, timer_html)
        self.assertContains(resp, text)

    def assertNotVLiveRedirects(self, resp, url):
        timer_html = '<TIMER href="%s' % url
        self.assertNotContains(resp, timer_html)
        
    def fill_in_basic_info(self):
        cv = self.get_user().get_profile()
        cv.first_name = 'Test'
        cv.surname = 'User'
        cv.gender = 'Male'
        cv.telephone_number = '0123456789'
        cv.date_of_birth = '01 Jan 1900'
        cv.highest_grade = '12'
        
        lang = Language(language = 'Afrikaans',  read_write = True)
        lang.save()
        cv.languages.add(lang)
        
        cv.save()

