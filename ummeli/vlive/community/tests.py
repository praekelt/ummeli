from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.base.models import StatusUpdate
from ummeli.opportunities.models import Job


class CommunityTestCase(VLiveTestCase):

    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
        'vlive/tests/article/fixtures/sample.json',
        'fixtures/opportunities.provinces.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        self.client.login(remote_user=self.msisdn)

    def test_community_post_listings(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)
        j = Job.objects.create(title='Test community job',
                               owner=user,
                               is_community=True,
                               state='published')
        j.save()
        i = StatusUpdate.objects.create(title='Test status update',
                                        owner=user,
                                        state='published')
        i.save()

        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].statusupdate.title, 'Test status update')

        resp = self.client.get(reverse('community_jobs'))
        self.assertContains(resp, 'Test community job')
        self.assertContains(resp, 'Test status update')
