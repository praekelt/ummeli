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

        self.assertEquals(data[0].category_set.count(),  5)
        self.assertEquals(data[1].category_set.count(),  2)

        self.assertEquals(data[0].category_set.all()[0].articles.count(),  5)
        self.assertEquals(data[1].category_set.all()[0].articles.count(),  4)

        resp = self.client.get(reverse('jobs_province'))
        self.assertContains(resp, 'Gauteng')

        resp = self.client.get(reverse('jobs_list', args=[1]))
        self.assertContains(resp, 'Accounts/Financial')

        resp = self.client.get(reverse('jobs', args=[1, 35]))
        self.assertContains(resp, '35')

        resp = self.client.get(reverse('job', args=[1, 35, 21]))
        self.assertContains(resp, 'Accounts Administrator West')

    def test_category_parser(self):
        items = JobsParser(html_str = jobs_test_data.articles_html1).parse()
        self.assertEquals(len(items),  4)

        self.assertRaises(Exception,  CategoryParser(2,  html_str = 'blah',  url = 'blah'))

    def test_job_apply_via_email(self):
        self.register()
        self.login()
        self.fill_in_basic_info()
        
        # setup test data
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser).result
        result.ready()
        result.successful()

        # apply via email
        resp = self.client.post(reverse('job', args=[1, 1, 1]),
                                        {'send_via':'email',  'send_to':'me@home.com'})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

    def test_job_apply_via_fax(self):
        self.register()
        self.login()
        self.fill_in_basic_info()
        
        # setup test data
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser).result
        result.ready()
        result.successful()

        # apply via fax
        resp = self.client.post(reverse('job', args=[1, 18, 10]),
                                        {'send_via':'fax',  'send_to':'+27123456789'})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')

        # test special launch special (max 2 faxes per user)
        self.assertEqual(self.get_user().get_profile().nr_of_faxes_sent,  1)

        # negative test case for require send_to
        resp = self.client.post(reverse('job', args=[1, 18, 10]),
                                        {'send_via':'fax',  'send_to':''})

        self.assertContains(resp,  'This field is required')
