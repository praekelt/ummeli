from functools import wraps
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

from ummeli.vlive.jobs.parsers import CategoryParser,  JobsParser
from ummeli.opportunities.models import Job, Province
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

    def test_job_data_creation(self):
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser)
        result.ready()
        result.successful()

        jobs = Job.objects.filter(category=1, province__province=Province.GAUTENG).count()
        self.assertEquals(jobs, 4)
        jobs = Job.objects.filter(province__province=Province.GAUTENG).count()
        self.assertEquals(jobs, 4)
        jobs = Job.objects.all().count()
        self.assertEquals(jobs, 9)

        resp = self.client.get(reverse('jobs_list'))
        self.assertContains(resp, 'Admin/Clerical')

        resp = self.client.get(reverse('jobs', args=[1]))
        self.assertContains(resp, 'Isando Bcom')

        slug = 'accounts-administrator-west-rand-kzn-limpopo-eebcompt-accounts-qualif-mon'
        resp = self.client.get(reverse('job', kwargs={'slug':slug}))
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
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser)
        result.ready()
        result.successful()

        # apply via email
        slug = 'accounts-administrator-west-rand-kzn-limpopo-eebcompt-accounts-qualif-mon'
        self.client.post(reverse('opportunity_apply', kwargs={'slug':slug}),
                                        {'send_via':'email',
                                         'send_to':'me@home.com'})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

    def test_job_apply_via_fax(self):
        self.register()
        self.login()
        self.fill_in_basic_info()

        # setup test data
        result = run_jobs_update.delay(MockCategoryParser,  MockJobsParser)
        result.ready()
        result.successful()

        # apply via fax

        resp = self.client.get(reverse('jobs', args=[1]))

        slug = 'accounts-administrator-west-rand-kzn-limpopo-eebcompt-accounts-qualif-mon'
        resp = self.client.post(reverse('opportunity_apply', kwargs={'slug':slug}),
                                        {'send_via':'fax',
                                         'send_to':'+27123456789'})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')

        # test special launch special (max 2 faxes per user)
        self.assertEqual(self.get_user().get_profile().nr_of_faxes_sent,  1)

        # negative test case for require send_to
        resp = self.client.post(reverse('opportunity_apply', kwargs={'slug':slug}),
                                        {'send_via':'fax',
                                         'send_to':''})
        self.assertContains(resp,  'Please enter a valid email')
