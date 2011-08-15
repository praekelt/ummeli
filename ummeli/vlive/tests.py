from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ummeli.api.utils import APIClient, UserHelper

import json
import urllib

class VliveTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def tearDown(self):
        pass
        
    def test_index_page(self):
        username = 'user'
        password = 'password'
        user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username, password)
        resp = self.client.get(reverse('vlive:index'))
        
        print resp.content
        self.assertEquals(resp.status_code, 302)