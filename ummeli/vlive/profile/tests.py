from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

from ummeli.base.models import (Certificate, Category, Province,
    CurriculumVitae)
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase


from neo4django import db
from ummeli.graphing.models import Person
from ummeli.graphing.utils import add_connection_for_user
import requests

def cleandb():
    key = getattr(settings, 'NEO4J_DELETE_KEY', None)
    server = getattr(settings, 'NEO4J_DATABASES', None)
    server = server.get(db.DEFAULT_DB_ALIAS, None) if server else None
    
    resp = requests.delete('http://%s:%s/cleandb/%s' %
                           (server['HOST'], str(server['PORT']), key))
    
    if resp.status_code != 200:
        print "\nTest database couldn't be cleared - have you installed the cleandb extension at https://github.com/jexp/neo4j-clean-remote-db-addon?"
        

class ProfileTestCase(VLiveTestCase):
    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
        'fixtures/skills.json',
    ]
    
    def setUp(self):
        cleandb()
        
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        settings.CELERY_ALWAYS_EAGER = True
        
    def tearDown(self):
        cleandb()
        settings.CELERY_ALWAYS_EAGER = settings.DEBUG

    def test_own_profile_page(self):
        #self.register()
        print User.objects.all()
        self.login()
        self.fill_in_basic_info()
        
        resp = self.client.get(reverse('profile'))
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Test User')
        self.assertContains(resp, 'Full Profile')
        
        user = User.objects.get(username=self.msisdn)
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Test User')
        
    def test_add_connection(self):
        other_msisdn = '27121111111' 
        self.login()
        self.fill_in_basic_info()
        
        user = User.objects.get(username=other_msisdn)
        user2 = User.objects.get(username='27122222222')
        
        profile = user.get_profile()
        profile.first_name = 'Joe'
        profile.surname = 'Blog'
        profile.save()
        
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        self.assertContains(resp, 'Joe Blog')
        self.assertNotContains(resp, 'Contact Info')
        
        resp = self.client.get(reverse('add_connection', args=[user.pk]))
        self.assertContains(resp, 'Joe Blog')
        
        resp = self.client.post(reverse('add_connection', args=[user.pk]))
        self.assertVLiveRedirects(resp, reverse('profile'))
        
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        self.assertContains(resp, 'request pending')
        
        resp = self.client.post(reverse('add_connection', args=[user2.pk]))
        self.assertVLiveRedirects(resp, reverse('profile'))
        
        resp = self.client.get(reverse('profile_view', args=[user2.pk]))
        self.assertContains(resp, 'request pending')
        
        self.logout()
        
        user = User.objects.get(username=self.msisdn)
        
        #User 2
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=other_msisdn)
        self.msisdn = other_msisdn
        self.login()
        resp = self.client.get(reverse('my_connections'))
        self.assertContains(resp, 'Connection Requests (1)')
        
        user = User.objects.get(username='27123456789')
        
        resp = self.client.get(reverse('confirm_request', args=[user.pk]))
        self.assertContains(resp, 'Test User')
        
        resp = self.client.post(reverse('confirm_request', args=[user.pk]))
        self.assertVLiveRedirects(resp, reverse('profile'))
        
        resp = self.client.get(reverse('my_connections'))
        self.assertContains(resp, 'My Connections (1)')
        
        self.logout()
        
        #User 1
        self.login()
        
        resp = self.client.get(reverse('my_connections'))
        self.assertContains(resp, 'My Connections (1)')
        
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        self.assertNotContains(resp, 'Full Profile')
        
        self.logout()
        
        #User 3
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID='27122222222')
        self.msisdn = '27122222222'
        self.login()
        
        resp = self.client.post(reverse('reject_request', args=[user.pk]))
        self.logout()
        
        #User 1
        
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID='27123456789')
        self.msisdn = '27123456789'
        self.login()
        
        resp = self.client.get(reverse('my_connections'))
        self.assertContains(resp, 'My Connections (1)')
        
        resp = self.client.get(reverse('profile_view', args=[user2.pk]))
        self.assertNotContains(resp, 'request pending')
        
        self.logout()
        
        #User 3
        self.login()
        
        resp = self.client.get(reverse('connections', args=[4]))
        self.assertContains(resp, 'Test User')
        
    def test_skills_views(self):
        self.login()
        self.fill_in_basic_info()
        
        resp = self.client.get(reverse('skills_new'))
        self.assertContains(resp, 'Accounts/Financial')
        
        #Add New
        resp = self.client.get(reverse('skills_new', args=[1]))
        self.assertContains(resp, 'Accounts/Financial')
        
        post_data = {
            'skill': 'Accounts/Financial',
            'level': 0,
        }
        
        resp = self.client.post(reverse('skills_new', args=[1]), post_data)
        resp = self.client.get(reverse('skills'))
        self.assertContains(resp,  'Accounts/Financial')
        self.assertContains(resp,  '(Laaitie)')
        
        #Mark as primary
        resp = self.client.get(reverse('skills_primary', args=[1]))
        resp = self.client.get(reverse('skills'))
        self.assertContains(resp, '*Accounts/Financial')
        
        #skills editing
        resp = self.client.get(reverse('skills', args=[1]))
        self.assertContains(resp, 'Accounts/Financial')
        
        post_data = {
            'level': 2,
            'skill': 'Accounts/Financial',
        }
        
        resp = self.client.post(reverse('skills', args=[1]), post_data)
        resp = self.client.get(reverse('skills'))
        self.assertContains(resp,  'Accounts/Financial')
        self.assertContains(resp,  '(Junior)')
        
        #Test Delete
        resp = self.client.get(reverse('skills_new', args=[2]))
        self.assertContains(resp,  'Admin/Clerical')
        
        post_data = {
            'level': 20,
            'skill': 'Admin/Clerical',
        }
        
        resp = self.client.post(reverse('skills_new', args=[2]), post_data)
        resp = self.client.get(reverse('skills'))
        self.assertContains(resp,  'Admin/Clerical')
        self.assertContains(resp,  '(Bozza)')
        
        resp = self.client.get(reverse('skills_delete', args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.post(reverse('skills_delete', args=[1]), post_data)
        resp = self.client.get(reverse('skills'))
        self.assertNotContains(resp,  'Accounts/Financial')
        
        #Test duplicate
        resp = self.client.post(reverse('skills_new', args=[2]), post_data)
        self.assertContains(resp,  'already added')