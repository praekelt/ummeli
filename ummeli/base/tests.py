from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ummeli.base.utils import render_to_pdf, convert_community_job_to_opportunity
from ummeli.opportunities.models import Job
from ummeli.base.models import UserSubmittedJobArticle, GAUTENG


class BaseTestCase(TestCase):
    fixtures = [
        'fixtures/opportunities.provinces.json',
    ]
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

    def test_community_job_to_opportunity_job(self):
        community_job = UserSubmittedJobArticle.objects.create(
            title='Sample Title',
            text='This is the description',
            province='Gauteng',
            job_category='Marketing',
            user=self.user
        )
        job = convert_community_job_to_opportunity(community_job)

        self.assertEquals(job.title, 'Sample Title')
        self.assertEquals(job.description, 'This is the description')
        self.assertEquals(job.category, 14)
        self.assertEquals(job.owner, self.user)
