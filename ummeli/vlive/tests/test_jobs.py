from functools import wraps
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from ummeli.vlive.jobs.parsers import CategoryParser,  JobsParser
from ummeli.base.models import Province,  Article,  Category
from ummeli.vlive.jobs.tasks import run_jobs_update
from ummeli.vlive.tests import jobs_test_data
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase


class MockCategoryParser(CategoryParser):
    def get_html(self,  url):
        if "search_source=2" in url:
            return self.tidy_html(jobs_test_data.categories_html1)
        return self.tidy_html(jobs_test_data.categories_html2)

class MockJobsParser(JobsParser):
    def get_html(self,  url):
        if "search_source=2" in url:
            return self.tidy_html(jobs_test_data.articles_html1)
        return self.tidy_html(jobs_test_data.articles_html2)

def reload_record(record):
    return record.__class__.objects.get(pk=record.pk)

class JobsTestCase(VLiveTestCase):
    def setUp(self):
        self.msisdn = '0123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        self.client.login(remote_user=self.msisdn)

    def test_job_data_creation(self):
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser).result
        result.ready()
        result.successful()
        data = result.join()

        self.assertEquals(data[0].category_set.count(),  42)
        self.assertEquals(data[1].category_set.count(),  47)

        self.assertEquals(data[0].category_set.all()[0].articles.count(),  10)
        self.assertEquals(data[1].category_set.all()[0].articles.count(),  10)

        resp = self.client.get(reverse('jobs_province'))
        self.assertContains(resp, 'Gauteng')

        resp = self.client.get(reverse('jobs_list', args=[1]))
        self.assertContains(resp, 'Accounts/Financial')

        resp = self.client.get(reverse('jobs',
                                        args=[1,  'df7288a55ea3f0826f1f2e61c74f3850']))
        self.assertContains(resp, 'b51556fd31b7a84d4a5cce22bf68dfe9')

        resp = self.client.get(reverse('job',
                                        args=[1,  'df7288a55ea3f0826f1f2e61c74f3850',
                                                'b51556fd31b7a84d4a5cce22bf68dfe9']))
        self.assertContains(resp, 'Accounts Administrator West')

    def test_category_parser(self):
        items = JobsParser(html_str = jobs_test_data.articles_html1).parse()
        self.assertEquals(len(items),  10)

        self.assertRaises(Exception,  CategoryParser(2,  html_str = 'blah',  url = 'blah'))

    def test_job_apply_via_email(self):
        self.register()
        self.login()
         # setup user's first_name and surname
        post_data = {
            'first_name': 'Test',
            'surname': 'User',
        }
        resp = self.client.post(reverse('edit_personal'), post_data)
        # setup test data
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser)

        # apply via email
        resp = self.client.post(reverse('job',
                                        args=[1,  'df7288a55ea3f0826f1f2e61c74f3850',
                                                'b51556fd31b7a84d4a5cce22bf68dfe9']),
                                        {'send_via':'email',  'send_to':'me@home.com',})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

    def test_job_apply_via_fax(self):
        self.register()
        self.login()

         # setup user's first_name and surname
        post_data = {
            'first_name': 'Test',
            'surname': 'User',
        }
        resp = self.client.post(reverse('edit_personal'), post_data)
        # setup test data
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser)

        # apply via fax
        profile = self.get_user().get_profile()
        self.assertEqual(profile.nr_of_faxes_sent, 0)
        resp = self.client.get(reverse('job',
                                        args=[
                                            1,
                                            'df7288a55ea3f0826f1f2e61c74f3850',
                                            'b51556fd31b7a84d4a5cce22bf68dfe9'
                                        ]), {
                                            'send_via': 'fax',
                                            'send_to': '+27123456789',
                                            '_action':'POST'
                                        })
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')

        # test special launch special (max 2 faxes per user)
        self.assertEqual(reload_record(profile).nr_of_faxes_sent,  1)

        # negative test case for require send_to
        resp = self.client.post(reverse('job',
                                        args=[
                                            1,
                                            'df7288a55ea3f0826f1f2e61c74f3850',
                                            'b51556fd31b7a84d4a5cce22bf68dfe9'
                                        ]), {
                                            'send_via': 'fax',
                                            'send_to': '',
                                        })

        self.assertContains(resp,  'This field is required')
