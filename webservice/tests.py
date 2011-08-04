"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.test import TestCase
from django.core.urlresolvers import reverse
from ummeli.webservice.utils import APIClient
from ummeli.webservice.models import *

class ApiTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.client.login('milton','password')
        #self.user = User.objects.get(username='milton')

    def tearDown(self):
        pass

    def test_get_data(self):
        resp = self.client.get(reverse('api:getuserdata', kwargs={'username':'milton'}))

        from django.utils import simplejson
        data = simplejson.loads(resp.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(resp.status_code, 200)
