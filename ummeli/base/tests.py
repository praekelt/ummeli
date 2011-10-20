from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ummeli.base.utils import render_to_pdf

class BaseTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        username = '0123456789'
        password = 'password'
        self.user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
    
    def tearDown(self):
        pass
        
    def test_convert_to_pdf(self):
        cv = self.user.get_profile()
        result = render_to_pdf('pdf_template.html', {'model': cv})
        self.assertNotEquals(result, None)
