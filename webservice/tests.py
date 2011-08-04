"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.test import TestCase
from django.core.urlresolvers import reverse
from ummeli.webservice.utils import APIClient
# import only what you need, importing * is handy but it could pull in lots
# of other stuff you weren't expecting. Explicit is better than implicit.
from ummeli.webservice.models import User
import json
import urllib

class ApiTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def tearDown(self):
        pass
    
    def test_get_data(self):
        # ensure the user account we're logging in with exists
        username = 'milton'
        password = 'password'
        
        user = User.objects.create(username=username, password=password)
        # this will expect that you're using the Django User model, it won't
        # actually do any authentication with your current view
        # self.client.login(username, password)
        
        # the reverse() function should refer to a URL as defined in your
        # urls.py, it's refered to with whatever 'name' you gave it.
        # Since you've removed the username parameter from the URL you
        # don't need to provide it anymore as a keyword argument. 
        resp = self.client.get('%s?%s' % (reverse('api:getuserdata'),
            urllib.urlencode({
                'username': username
            }))
        )
        
        print resp.content
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEquals(len(data), 1)
