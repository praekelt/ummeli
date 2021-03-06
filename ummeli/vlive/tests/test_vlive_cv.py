from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings

from ummeli.base.models import CurriculumVitae
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import Job

class VLiveCVTestCase(VLiveTestCase):
    fixtures = [
        'fixtures/opportunities.provinces.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        self.client.login(remote_user=self.msisdn)
        settings.CELERY_ALWAYS_EAGER = True

    def tearDown(self):
        settings.CELERY_ALWAYS_EAGER = settings.DEBUG

    def test_edit_personal_page(self):
        resp = self.client.get(reverse('profile'))
        self.assertEquals(resp.status_code, 200)

        resp = self.client.get(reverse('edit_personal'))
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'first_name': 'Milton',
            'surname': 'Madanda',
            'gender': 'Male',
        }
        # not provided pin yet so it should redirect
        resp = self.client.post(reverse('edit_personal'), post_data)
        self.assertVLiveRedirects(resp, reverse('register'))
        # register pin
        resp = self.register()

        # try again, this time after having set the pin
        resp = self.client.post(reverse('edit_personal'), post_data)
        cv = self.get_user().get_profile()
        self.assertEquals(cv.first_name, 'Milton')
        self.assertEquals(cv.surname, 'Madanda')
        self.assertEquals(cv.gender, 'Male')
        # reload the page and check for new entries in form
        resp = self.client.get(reverse('edit_personal'))
        self.assertContains(resp, 'Milton')
        self.assertContains(resp, 'Madanda')
        self.assertContains(resp, 'Male')
        # logout & login
        resp = self.logout()

        # not provided pin yet so it should redirect to login page
        resp = self.client.post(reverse('edit_personal'), post_data)
        self.assertVLiveRedirects(resp, reverse('login'))

        # FIXME: we shouldn't need to provide the MSISDN here.
        resp = self.login()
        # load the personal details again, ensure they're present
        resp = self.client.get(reverse('edit_personal'))
        self.assertContains(resp, 'Male')
        self.assertContains(resp, 'Milton')
        self.assertContains(resp, 'Madanda')

    def test_edit_contact_details_page(self):
        self.register()
        self.login()

        resp = self.client.get(reverse('profile'))
        self.assertEquals(resp.status_code, 200)

        resp = self.client.get(reverse('edit_contact'))
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'telephone_number': '0123456978',
            'address': 'Oak Rd',
            'city': 'Durban',
            'province': '1',
        }
        resp = self.client.post(reverse('edit_contact'), post_data)

        cv = self.get_user().get_profile()
        self.assertEquals(cv.telephone_number, '0123456978')
        self.assertEquals(cv.address, 'Oak Rd')
        self.assertEquals(cv.city, 'Durban')

    def test_edit_education_details_page(self):

        resp = self.client.get(reverse('profile'))
        self.assertEquals(resp.status_code, 200)
        self.assertVLiveRedirects(resp, reverse('register'))
        self.register()
        self.login()

        resp = self.client.get(reverse('edit_education'))
        self.assertNotVLiveRedirects(resp, reverse('login'))

        post_data = {
            'highest_grade': '12',
            'highest_grade_year': 2005,
            'school': 'Some school'
        }
        resp = self.client.post(reverse('edit_education'), post_data)

        cv = self.get_user().get_profile()
        self.assertEquals(cv.highest_grade, '12')
        self.assertEquals(cv.highest_grade_year, 2005)
        self.assertEquals(cv.school, 'Some school')

    def test_edit_certificates_details_page(self):
        resp = self.client.get(reverse('profile'))
        self.assertVLiveRedirects(resp, reverse('register'))

         # test certificates listing
        resp = self.client.get(reverse('certificate_list'))

         # test certificates add form
        resp = self.client.get(reverse('certificate_new'))
        self.assertVLiveRedirects(resp, reverse('register'))

        self.register()
        self.login()

         # test certificates add action
        post_data = {
            'name': 'BSc',
            'institution': 'UCT',
            'year': 2007,
        }
        resp = self.client.post(reverse('certificate_new'),  post_data)

         # test certificates listing of new certificate
        resp = self.client.get(reverse('certificate_list'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'BSc')

         # test editing of created certificate
        resp = self.client.get(reverse('certificate_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'name': 'BSc in IT',
            'institution': 'UCT',
            'year': 2007,
        }
        resp = self.client.post(reverse('certificate_edit', args=[1]),
                                post_data)

        resp = self.client.get(reverse('certificate_list'))
        self.assertContains(resp, 'BSc in IT')
        certs = self.get_user().get_profile().certificates.all()
        self.assertEquals(certs.count(), 1)

         # test delete action
        resp = self.client.get(reverse('certificate_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')

        resp = self.client.post(reverse('certificate_delete',  args=[1]))
        certs = self.get_user().get_profile().certificates.all()
        self.assertEquals(certs.count(), 0)

    def test_edit_work_experiences_details_page(self):

        self.register()
        self.login()

        resp = self.client.get(reverse('profile'))
        self.assertNotVLiveRedirects(resp, reverse('login'))

         # test certificates listing
        resp = self.client.get(reverse('work_experience_list'))
        self.assertNotVLiveRedirects(resp, reverse('login'))

         # test certificates add form
        resp = self.client.get(reverse('workExperience_new'))
        self.assertNotVLiveRedirects(resp, reverse('login'))

         # test certificates add action
        post_data = {
            'title': 'Engineer',
            'company': 'Praekelt',
            'start_year': 2007,
            'end_year': 2008,
        }
        # TODO: fix camel casing
        resp = self.client.post(reverse('workExperience_new'),  post_data)

         # test certificates listing of new certificate
        resp = self.client.get(reverse('work_experience_list'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Praekelt')

         # test editing of created certificate
        resp = self.client.get(reverse('workExperience_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'title': 'Engineer',
            'company': 'Praekelt Consulting',
            'start_year': 2007,
            'end_year': 2008,
        }
        resp = self.client.post(reverse('workExperience_edit', args=[1]),
                                post_data)

        resp = self.client.get(reverse('work_experience_list'))
        self.assertContains(resp, 'Praekelt Consulting')

        work_experiences = self.get_user().get_profile().work_experiences.all()
        self.assertEquals(work_experiences.count(), 1)

         # test delete action
        resp = self.client.get(reverse('workExperience_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')

        resp = self.client.post(reverse('workExperience_delete',  args=[1]))
        work_experiences = self.get_user().get_profile().work_experiences.all()
        self.assertEquals(work_experiences.count(), 0)

    def test_edit_languages_details_page(self):
        self.register()
        self.login()

        resp = self.client.get(reverse('profile'))
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

         # test editing of created language
        resp = self.client.get(reverse('language_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {'language': 'Afrikaans', 'read_write': True}
        resp = self.client.post(reverse('language_edit', args=[1]),
                                post_data)

        resp = self.client.get(reverse('language_list'))
        self.assertContains(resp, 'Afrikaans')

        languages = self.get_user().get_profile().languages.all()
        self.assertEquals(languages.count(), 1)

         # test delete action
        resp = self.client.get(reverse('language_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')

        resp = self.client.post(reverse('language_delete',  args=[1]))
        languages = self.get_user().get_profile().languages.all()
        self.assertEquals(languages.count(), 0)

    def test_edit_references_details_page(self):
        self.register()
        self.login()

        resp = self.client.get(reverse('profile'))
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

        references = self.get_user().get_profile().references
        self.assertEquals(len(references.all()), 1)

         # test delete action
        resp = self.client.get(reverse('reference_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')

        resp = self.client.post(reverse('reference_delete',  args=[1]))
        references = self.get_user().get_profile().references
        self.assertEquals(len(references.all()), 0)

    def test_email(self):
        # setup user's first_name and surname
        self.register()
        self.login()
        self.fill_in_basic_info()

        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)

        post_data = {'send_to': 'madandat@gmail.com', 'send_via': 'email'}
        resp = self.client.post(reverse('send'), post_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')
        self.assertEqual(mail.outbox[0].bcc[0], 'ummeli@praekeltfoundation.org')
        self.assertEqual(mail.outbox[0].from_email, settings.SEND_FROM_EMAIL_ADDRESS)

    def test_fax(self):
        # setup user's first_name and surname
        self.register()
        self.login()
        self.fill_in_basic_info()

        post_data = {
            'send_to': '+27123456789',
            'send_via': 'fax'
        }
        resp = self.client.post(reverse('send'), post_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')
        self.assertEqual(mail.outbox[0].bcc[0], 'ummeli@praekeltfoundation.org')
        self.assertEqual(mail.outbox[0].from_email, settings.SEND_FROM_FAX_EMAIL_ADDRESS)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

        self.assertEqual(self.get_user().get_profile().nr_of_faxes_sent,  1)

    def test_missing_fields_when_sending(self):
        # setup user's first_name and surname
        self.register()
        self.login()

        post_data = {'send_to': 'madandat@gmail.com', 'send_via': 'email'}
        resp = self.client.post(reverse('send'), post_data)

        self.assertContains(resp,  'Your CV is incomplete')
        self.assertContains(resp,  'first name')
        self.assertContains(resp,  'gender')

    def test_job_creation(self):
        self.register()
        self.login()

        post_data = {
            'province': '2',
            'category': '6',
            'title': 'Plumber needed',
            'description': 'This is some sample text.',
        }
        resp = self.client.post(reverse('jobs_create'), post_data)
        self.assertEqual(Job.objects.all().count(), 1)

        #test shows in my jobs
        resp = self.client.get(reverse('my_jobs'))
        self.assertContains(resp,  'Plumber needed')

        #test can edit job
        resp = self.client.get(reverse('my_jobs', args=[1]))
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'province': '2',
            'category': '6',
            'title': 'Plumber needed 2',
            'description': 'This is some sample text.',
        }
        resp = self.client.post(reverse('jobs_create'), post_data)
        print resp
        self.assertEqual(Job.objects.all().count(), 2)

        resp = self.client.get(reverse('my_jobs'))
        self.assertContains(resp,  'Plumber needed 2')

        #test duplicate submissions
        resp = self.client.post(reverse('jobs_create'), post_data)
        self.assertEqual(Job.objects.all().count(), 2)

        post_data = {
            'province': '2',
            'category': '0',
            'title': 'Plumber needed',
            'description': 'This is some sample text.',
        }
        resp = self.client.post(reverse('jobs_create'), post_data)
        self.assertContains(resp,  'Please choose a category.')

    def test_cv_is_complete(self):
        # setup user's first_name and surname
        self.register()
        self.login()
        self.fill_in_basic_info()

        cv = self.get_user().get_profile()
        # remove a required field
        cv.telephone_number = None
        cv.save()
        # reload & check to ensure that is the case
        cv = CurriculumVitae.objects.get(pk=cv.pk)
        self.assertTrue(cv.missing_fields())
        self.assertEquals(cv.is_complete,  False)

        post_data = {
            'telephone_number': '0123456978',
            'address': 'Oak Rd',
            'city': 'Durban',
            'province': '1',
        }
        resp = self.client.post(reverse('edit_contact'), post_data)
        cv = self.get_user().get_profile()

        self.assertEquals(cv.is_complete,  True)
