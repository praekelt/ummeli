from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from ummeli.vlive.utils import render_to_pdf
from ummeli.api.models import Certificate

import json
import urllib

class VliveTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def tearDown(self):
        pass
        
    def test_index_page(self):
        username = 'user'
        password = 'password'
        user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse('index'))
         #  there shouldn't be a Location header as this would mean a redirect
         #  to a login URL
        self.assertEquals(resp.get('Location', None), None)
        self.assertEquals(resp.status_code, 200)
        
    def test_login_view(self):
        msisdn = '0123456789'
        password = 'password'
        user = User.objects.create_user(msisdn, '%s@domain.com' % msisdn, 
                                        password)
        resp = self.client.get(reverse('login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': password, 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        self.assertEquals(resp.status_code, 200)  # redirect to index
        self.assertContains(resp, 'Edit CV')
        
        resp = self.client.get(reverse('login'), 
                               {'password': 'wrong_pin', '_action': 'POST'},
                                HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        self.assertEquals(resp.status_code, 200)      
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('index'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        #self.assertEquals(resp.status_code, 302)  # redirect to login
        #self.assertEquals(resp.get('Location', None), 
        #                'http://testserver/vlive/login?next=/vlive/')
        
        resp = self.client.get(reverse('login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Click here to create profile.')
        
        resp = self.client.get(reverse('register'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Create pin for %s' % (msisdn))
        
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password, 
                                'password2': password,  '_action': 'POST'},  
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Enter Pin to sign in.')
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': password, 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Edit CV')

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('register'), 
                               {'username': msisdn, 'password1': password, 
                               'password2': 'wrong',  '_action': 'POST'}, 
                               HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        print resp
        self.assertContains(resp, 'Pin codes don&apos;t match.')
        

class VliveCVTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        username = 'user'
        password = 'password'
        self.user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
    
    def tearDown(self):
        pass
        
    def test_edit_personal_page(self):
        msisdn = '0123456789'
        
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('edit'), 
                                        'personal'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'firstName': 'Milton', 'gender': 'Male',  
                        '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.firstName, 'Milton')
        self.assertEquals(cv.gender, 'Male')
            
    def test_edit_contact_details_page(self):
        msisdn = '0123456789'
        
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('edit'), 
                                        'contact'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'telephoneNumber': '0123456978', 'streetName': 'Oak Rd', 
                     '_action': 'POST'}
        resp = self.client.get(reverse('edit_contact'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.telephoneNumber, '0123456978')
        self.assertEquals(cv.streetName, 'Oak Rd')
        
    def test_edit_education_details_page(self):
        msisdn = '0123456789'
        
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('edit'), 
                                        'education'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'highestGrade': '12', 'highestGradeYear': 2005,
                    'school': 'Some school',  '_action': 'POST'}
        resp = self.client.get(reverse('edit_education'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.highestGrade, '12')
        self.assertEquals(cv.highestGradeYear, 2005)
        self.assertEquals(cv.school, 'Some school')

    def test_edit_certificates_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates listing
        resp = self.client.get(reverse('certificate_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add form
        resp = self.client.get(reverse('certificate_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add action
        post_data = {'name': 'BSc', 'institution': 'UCT', 'year': 2007}
        resp = self.client.post(reverse('certificate_new'),  post_data)
        
         # test certificates listing of new certificate
        resp = self.client.get(reverse('certificate_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'BSc')
        
         # test editing of created certificate
        resp = self.client.get(reverse('certificate_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'name': 'BSc in IT', 'institution': 'UCT', 'year': 2007}
        resp = self.client.post(reverse('certificate_edit', args=[1]),  
                                post_data)
        
        resp = self.client.get(reverse('certificate_list'))
        self.assertContains(resp, 'BSc in IT')
        
        certs = self.user.get_profile().certificates
        self.assertEquals(len(certs.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('certificate_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('certificate_delete',  args=[1]))
        certs = self.user.get_profile().certificates
        self.assertEquals(len(certs.all()), 0)        

    def test_edit_workExperiences_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates listing
        resp = self.client.get(reverse('workExperience_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add form
        resp = self.client.get(reverse('workExperience_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add action
        post_data = {'title': 'Engineer', 'company': 'Praekelt', 
                    'startYear': 2007, 'endYear': 2008}
        resp = self.client.post(reverse('workExperience_new'),  post_data)
        
         # test certificates listing of new certificate
        resp = self.client.get(reverse('workExperience_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Praekelt')
        
         # test editing of created certificate
        resp = self.client.get(reverse('workExperience_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'title': 'Engineer', 'company': 'Praekelt Consulting', 
                    'startYear': 2007, 'endYear': 2008}
        resp = self.client.post(reverse('workExperience_edit', args=[1]),  
                                post_data)
        print resp
        resp = self.client.get(reverse('workExperience_list'))
        self.assertContains(resp, 'Praekelt Consulting')
        
        workExperiences = self.user.get_profile().workExperiences
        self.assertEquals(len(workExperiences.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('workExperience_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('workExperience_delete',  args=[1]))
        workExperiences = self.user.get_profile().workExperiences
        self.assertEquals(len(workExperiences.all()), 0)
        
    def test_edit_languages_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test languages listing
        resp = self.client.get(reverse('language_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test language add form
        resp = self.client.get(reverse('language_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test languageadd action
        post_data = {'language': 'English', 'readWrite': True}
        resp = self.client.post(reverse('language_new'),  post_data)
        
         # test listing of new language
        resp = self.client.get(reverse('language_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'English')
        
         # test editing of created certificate
        resp = self.client.get(reverse('language_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'language': 'Afrikaans', 'readWrite': True}
        resp = self.client.post(reverse('language_edit', args=[1]),  
                                post_data)
        
        resp = self.client.get(reverse('language_list'))
        self.assertContains(resp, 'Afrikaans')
        
        languages = self.user.get_profile().languages
        self.assertEquals(len(languages.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('language_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('language_delete',  args=[1]))
        languages = self.user.get_profile().languages
        self.assertEquals(len(languages.all()), 0)        
        
    def test_edit_references_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test references listing
        resp = self.client.get(reverse('reference_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test reference add form
        resp = self.client.get(reverse('reference_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test reference add action
        post_data = {'fullname': 'Test', 'relationship': 'Manager'}
        resp = self.client.post(reverse('reference_new'),  post_data)
        
         # test listing of new reference
        resp = self.client.get(reverse('reference_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Test')
        
         # test editing of created reference
        resp = self.client.get(reverse('reference_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'fullname': 'User', 'relationship': 'Manager'}
        resp = self.client.post(reverse('reference_edit', args=[1]),  
                                post_data)
        
        resp = self.client.get(reverse('reference_list'))
        self.assertContains(resp, 'User')
        
        references = self.user.get_profile().references
        self.assertEquals(len(references.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('reference_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('reference_delete',  args=[1]))
        references = self.user.get_profile().references
        self.assertEquals(len(references.all()), 0)                
        
    def test_convert_to_pdf(self):
        cv = self.user.get_profile()
        result = render_to_pdf('vlive/pdf_template.html', {'model': cv})
        self.assertEquals(result == None, False)

    def test_email(self):
        msisdn = '0123456789'
        
         # setup user's firstName and surname
        post_data = {'firstName': 'Test', 'surname': 'User',  
        '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
                                        
        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('send'), 'email'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'email': 'madandat@gmail.com'}
        resp = self.client.post('%s/%s' % (reverse('send'), 
                                        'email'), post_data)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

    def test_fax(self):
        msisdn = '0123456789'
        
         # setup user's firstName and surname
        post_data = {'firstName': 'Test', 'surname': 'User', 
                     '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
                                        
        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('send'), 'fax'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'fax': '+27123456789'}
        resp = self.client.post('%s/%s' % (reverse('send'), 
                                        'fax'), post_data)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@ummeli.org')
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')
        
