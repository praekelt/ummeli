from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from ummeli.base.models import Certificate, Category, Province

import json
import urllib

class VliveCVTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        username = '0123456789'
        password = 'password'
        self.user = User.objects.create_user(username, '%s@domain.com' % username,
                                        password)
        self.client.login(username=username, password=password)

    def tearDown(self):
        pass

    def test_edit_personal_page(self):
        msisdn = '0123456789'
        password = 'password'

        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)

        resp = self.client.get(reverse('edit_personal'))
        self.assertEquals(resp.status_code, 200)

        post_data = {'first_name': 'Milton', 'surname': 'Madanda',
                            'gender': 'Male',  '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data,
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)

        cv = self.user.get_profile()
        self.assertEquals(cv.first_name, 'Milton')
        self.assertEquals(cv.surname, 'Madanda')
        self.assertEquals(cv.gender, 'Male')

        resp = self.client.get(reverse('edit_personal'))
        self.assertContains(resp, 'Milton')
        self.assertContains(resp, 'Madanda')
        self.assertContains(resp, 'Male')

        self.client.get(reverse('logout'))
        self.client.get(reverse('login'),
                                {'username': msisdn, 'password': password,
                                '_action': 'POST'},
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        resp = self.client.get(reverse('edit_personal'))

        self.assertContains(resp, 'Male')
        self.assertContains(resp, 'Milton')
        self.assertContains(resp, 'Madanda')

    def test_edit_contact_details_page(self):
        msisdn = '0123456789'

        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)

        resp = self.client.get(reverse('edit_contact'))
        self.assertEquals(resp.status_code, 200)

        post_data = {'telephone_number': '0123456978', 'street_name': 'Oak Rd',
                     '_action': 'POST'}
        resp = self.client.get(reverse('edit_contact'), post_data,
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)

        cv = self.user.get_profile()
        self.assertEquals(cv.telephone_number, '0123456978')
        self.assertEquals(cv.street_name, 'Oak Rd')

    def test_edit_education_details_page(self):
        msisdn = '0123456789'

        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)

        resp = self.client.get(reverse('edit_education'))
        self.assertEquals(resp.status_code, 200)

        post_data = {'highest_grade': '12', 'highest_grade_year': 2005,
                    'school': 'Some school',  '_action': 'POST'}
        resp = self.client.get(reverse('edit_education'), post_data,
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)

        cv = self.user.get_profile()
        self.assertEquals(cv.highest_grade, '12')
        self.assertEquals(cv.highest_grade_year, 2005)
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

    def test_edit_work_experiences_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)

         # test certificates listing
        resp = self.client.get(reverse('work_experience_list'))
        self.assertEquals(resp.status_code, 200)

         # test certificates add form
        resp = self.client.get(reverse('workExperience_new'))
        self.assertEquals(resp.status_code, 200)

         # test certificates add action
        post_data = {'title': 'Engineer', 'company': 'Praekelt',
                    'start_year': 2007, 'end_year': 2008}
        resp = self.client.post(reverse('workExperience_new'),  post_data)

         # test certificates listing of new certificate
        resp = self.client.get(reverse('work_experience_list'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Praekelt')

         # test editing of created certificate
        resp = self.client.get(reverse('workExperience_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {'title': 'Engineer', 'company': 'Praekelt Consulting',
                    'start_year': 2007, 'end_year': 2008}
        resp = self.client.post(reverse('workExperience_edit', args=[1]),
                                post_data)
        print resp
        resp = self.client.get(reverse('work_experience_list'))
        self.assertContains(resp, 'Praekelt Consulting')

        work_experiences = self.user.get_profile().work_experiences
        self.assertEquals(len(work_experiences.all()), 1)

         # test delete action
        resp = self.client.get(reverse('workExperience_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')

        resp = self.client.post(reverse('workExperience_delete',  args=[1]))
        work_experiences = self.user.get_profile().work_experiences
        self.assertEquals(len(work_experiences.all()), 0)

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
        post_data = {'language': 'English', 'read_write': True}
        resp = self.client.post(reverse('language_new'),  post_data)

         # test listing of new language
        resp = self.client.get(reverse('language_list'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'English')

         # test editing of created certificate
        resp = self.client.get(reverse('language_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {'language': 'Afrikaans', 'read_write': True}
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
        post_data = {'fullname': 'Test', 'relationship': 'Manager',
                            'contact_no': '0123456789'}
        resp = self.client.post(reverse('reference_new'),  post_data)

         # test listing of new reference
        resp = self.client.get(reverse('reference_list'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Test')

         # test editing of created reference
        resp = self.client.get(reverse('reference_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {'fullname': 'User', 'relationship': 'Manager',
                            'contact_no': '0123456789'}
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

    def test_email(self):
        msisdn = '0123456789'

         # setup user's first_name and surname
        post_data = {'first_name': 'Test', 'surname': 'User',
        '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data,
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)

        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)

        post_data = {'send_to': 'madandat@gmail.com', 'send_via': 'email'}
        resp = self.client.post(reverse('send'), post_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

    def test_fax(self):
        msisdn = '0123456789'

         # setup user's first_name and surname
        post_data = {'first_name': 'Test', 'surname': 'User',
                     '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data,
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)

        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)

        post_data = {'send_to': '+27123456789',  'send_via': 'fax'}
        resp = self.client.post(reverse('send'), post_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

        self.assertEqual(self.user.get_profile().nr_of_faxes_sent,  1)

    def test_job_creation(self):
        msisdn = '0123456789'

        Province(search_id = 2,  name = 'Gauteng').save()
        Province(search_id = 5,  name = 'Western Cape').save()
        Province(search_id = 6,  name = 'KZN').save()

        post_data = {'province': '2', 'category': 'Engineering',
                            'title': 'Plumber needed',  'text': 'This is some sample text.'}
        resp = self.client.post(reverse('jobs_create'), post_data,
                                HTTP_X_UP_CALLING_LINE_ID=msisdn)

        self.assertEqual(Category.objects.count(), 1)

        post_data = {'province': '', 'category': 'Engineering',
                            'title': 'Plumber needed',  'text': 'This is some sample text.'}
        resp = self.client.post(reverse('jobs_create'), post_data,
                                HTTP_X_UP_CALLING_LINE_ID=msisdn)
        print resp
        self.assertContains(resp,  'Province - This field is required')
