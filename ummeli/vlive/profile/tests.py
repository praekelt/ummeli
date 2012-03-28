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

    def setUp(self):
        cleandb()
        
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        self.client.login(remote_user=self.msisdn)
        settings.CELERY_ALWAYS_EAGER = True
        
    def tearDown(self):
        cleandb()
        settings.CELERY_ALWAYS_EAGER = settings.DEBUG

    def test_own_profile_page(self):
        self.register()
        self.login()
        self.fill_in_basic_info()
        
        resp = self.client.get(reverse('profile'))
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Test User')
        self.assertContains(resp, '[edit]')
        
        user = User.objects.get(username=self.msisdn)
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Test User')
        self.assertContains(resp, '[edit]')
        
    def test_add_connection(self):
        self.register()
        self.register('0123456789')
        self.login()
        self.fill_in_basic_info()
        
        user = User.objects.get(username='0123456789')
        profile = user.get_profile()
        profile.first_name = 'Joe'
        profile.surname = 'Blog'
        profile.save()
        
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        self.assertContains(resp, 'Joe Blog')
        
        resp = self.client.get(reverse('add_connection', args=[user.pk]))
        self.assertContains(resp, 'Joe Blog')
        
        resp = self.client.post(reverse('add_connection', args=[user.pk]))
        self.assertVLiveRedirects(resp, reverse('profile'))
        
        resp = self.client.get(reverse('profile_view', args=[user.pk]))
        print resp
        self.assertContains(resp, 'request pending')