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
import json

class ApiTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.client.login('milton','password')
        #self.user = User.objects.get(username='milton')

    def tearDown(self):
        pass

    def test_get_data(self):
        resp = self.client.get(reverse('api:getuserdata_with_name', kwargs={
            'username':'milton'}))
        
        self.assertEquals(resp.status_code, 200)
        print resp.content
        data = json.loads(resp.content)
        self.assertEquals(len(data), 1)
