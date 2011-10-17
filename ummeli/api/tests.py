from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from piston.utils import rc

from ummeli.api.utils import APIClient, UserHelper
from ummeli.api.models import CurriculumVitae

import json
import urllib

class ApiTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def tearDown(self):
        pass
        
    def test_get_data(self):
        username = 'user'
        password = 'password'
        user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': username,
                'password': password
            }))
        )
        
        self.assertEquals(resp.status_code, rc.ALL_OK.status_code)
        data = json.loads(resp.content)
        self.assertEquals(len(data), 16)
        

    def test_get_data_for_invalid_user(self):
        username = 'user'
        password = 'password'
        
        user = User.objects.create(username=username, password=password)
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': 'wronguser'
            }))
        )
        
        print resp.content
        self.assertEquals(resp.status_code, 403)  # Forbidden
    
    def test_registration(self):
        username = 'user'
        password = 'password'

        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        data = json.loads(resp.content)
        self.assertEquals(len(data), 16)
        
        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        self.assertEquals(resp.status_code, rc.DUPLICATE_ENTRY.status_code)
        
    def test_cv_updating(self):
        username = 'user'
        password = 'password'

        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        cv = {
                'telephoneNumber': '0123456789', 
                'school': None, 
                'surname': 'surname', 
                'highestGrade': None, 
                'firstName': 'name', 
                'gender': 'male', 
                'workExperiences': [], 
                'languages': [], 
                'dateOfBirth': None, 
                'references': [], 
                'location': None, 
                'certificates': [], 
                'highestGradeYear': 0, 
                'houseNumber': None, 
                'email': 'an@email.com', 
                'streetName': None,
                'username': username,
                'password': password
            }
        resp = self.client.put(reverse('api:userdata'),cv)
        
        self.assertEquals(resp.status_code, rc.ALL_OK.status_code)
        
        cv = {
                'telephoneNumber': '0123456789', 
                'school': 'Some school', 
                'surname': 'surname', 
                'highestGrade': '12', 
                'firstname': 'name', 
                'gender': 'male', 
                'workExperiences': [], 
                'languages': [], 
                'dateOfBirth': None, 
                'references': [], 
                'location': None, 
                'certificates': [], 
                'highestGradeYear': 0, 
                'houseNumber': None, 
                'email': 'an@email.com', 
                'streetName': None,
                'username': username,
                'password': password
            }
        resp = self.client.put(reverse('api:userdata'),cv)
        
        self.assertEquals(resp.status_code, rc.ALL_OK.status_code)
        
        cv = User.objects.get(username = username).get_profile()
        self.assertEquals(cv.school,'Some school')
        self.assertEquals(cv.highestGrade,'12')
        
    def test_authentication(self):
        username = 'user'
        password = 'password'

        resp = self.client.post(reverse('api:userdata'),
                                {'username': username,'password': password})
        
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': username,
                'password': password
            }))
        )
        self.assertEquals(resp.status_code, rc.ALL_OK.status_code)
        
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': username,
                'password': 'wrong_password'
            }))
        )
        self.assertEquals(resp.status_code, 403)  # Forbidden
        
        user = UserHelper.get_user_or_403(username, password)
        user.is_active = False  # test for user disabled
        user.save()
        
        resp = self.client.get('%s?%s' % (reverse('api:userdata'),
            urllib.urlencode({
                'username': username,
                'password': password
            }))
        )
        
        self.assertEquals(resp.status_code, 403)  # forbidden
