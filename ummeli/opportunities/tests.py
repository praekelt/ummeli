from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import Opportunity


class OpportunitiesTest(VLiveTestCase):
    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)

    def test_basic_opportunity(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        Opportunity.objects.create(title='Test op',
                                    description='This is a test',
                                    provider=user)
        print dir(user)
        self.assertEqual(user.opportunity_set.count(), 1)
        self.assertEqual(user.opportunity_set.all()[0].deadline, None)
