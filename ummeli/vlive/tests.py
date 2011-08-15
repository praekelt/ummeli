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
        # there shouldn't be a Location header as this would mean a redirect
        # to a login URL
        self.assertEquals(resp.get('Location', None), None)
        self.assertEquals(resp.status_code, 200)