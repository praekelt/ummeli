from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import *
from reporting import helpers
from mock import patch
import fakeredis

from django.core.urlresolvers import reverse

def mock_redis(**kwargs):
    return fakeredis.FakeStrictRedis()


@patch('redis.StrictRedis', mock_redis)
class ReportingTest(VLiveTestCase):
    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn,
                                  HTTP_REFERER='/')

    def test_reporting_on_training(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        t = Training.objects.create(title='Test op 1',
                                    description='This is a test',
                                    owner=user)
        kwargs = {'slug': t.slug,
                  'report_key_field': UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD
        }
        self.client.get(reverse('report_object', kwargs=kwargs))

        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 1)

        #test duplicate votes
        self.client.get(reverse('report_object', kwargs=kwargs))
        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 1)

        #test vote by other user
        self.logout()
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID='27121111111',
                                  HTTP_REFERER='/')
        self.client.get(reverse('report_object', kwargs=kwargs))

        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 2)

    def test_reporting_on_different_opportunities(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        t = Training.objects.create(title='Test op 2',
                                    description='This is a test',
                                    owner=user)

        v = Volunteer.objects.create(title='Test Volunteer 2',
                                    description='This is a test Volunteer',
                                    owner=user)

        kwargs = {'slug': t.slug,
                  'report_key_field': UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD
        }
        self.client.get(reverse('report_object', kwargs=kwargs))

        kwargs = {'slug': v.slug,
                  'report_key_field': UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD
        }
        self.client.get(reverse('report_object', kwargs=kwargs))

        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 1)

        self.assertEquals(helpers.get_object_votes(v, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 1)

    def test_reporting_on_different_keys(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        t = Training.objects.create(title='Test op 3',
                                    description='This is a test',
                                    owner=user)

        kwargs = {'slug': t.slug,
                  'report_key_field': UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD
        }
        self.client.get(reverse('report_object', kwargs=kwargs))

        kwargs = {'slug': t.slug,
                  'report_key_field': UmmeliOpportunity.SCAM_REPORT_KEY_FIELD
        }
        self.client.get(reverse('report_object', kwargs=kwargs))

        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 1)
        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.SCAM_REPORT_KEY_FIELD), 1)


    def test_flagging_of_models_to_be_removed(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        t = Training.objects.create(title='Test op 4',
                                    description='This is a test',
                                    owner=user)

        kwargs = {'slug': t.slug,
                  'report_key_field': UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD
        }
        self.client.get(reverse('report_object', kwargs=kwargs))

        self.logout()
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID='27121111111',
                                  HTTP_REFERER='/')
        self.client.get(reverse('report_object', kwargs=kwargs))

        self.assertEquals(helpers.get_object_votes(t, UmmeliOpportunity.ABUSE_REPORT_KEY_FIELD), 2)
