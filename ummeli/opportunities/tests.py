from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import Internship, Salary, Training, Event,\
                                            Province
from django.core.urlresolvers import reverse


class OpportunitiesTest(VLiveTestCase):
    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
        'fixtures/opportunities.provinces.json',
        'opportunities/fixtures/test.opportunities.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)

    def test_internship(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        salary = Salary(amount=50, frequency=1)
        salary.save()

        i = Internship.objects.create(title='Test op',
                                    description='This is a test',
                                    owner=user,
                                    salary=salary,
                                    state='published')
        i.province.add(2)
        i.province.add(3)
        i.save()

        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].internship.salary.amount, 50)
        self.assertEqual(user.modelbase_set.all()[0].internship.education, 0)
        self.assertEqual(user.modelbase_set.all()[0].internship.province.count(), 2)

        resp = self.client.get(reverse('internships'))
        self.assertContains(resp, 'Test op')

        resp = self.client.get(reverse('internship_detail', kwargs={'slug': 'test-op'}))
        self.assertContains(resp, 'Test op')
        self.assertContains(resp, 'This is a test')

    def test_training(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        i = Training.objects.create(title='Test op',
                                    description='This is a test',
                                    owner=user,
                                    cost=300)
        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].training.cost, 300)

    def test_event(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        i = Event.objects.create(title='Test op',
                                    description='This is a test',
                                    owner=user,
                                    location='Salt River')
        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].event.location, 'Salt River')

    def test_change_province_session(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)
        province = Province.objects.get(province=3)
        i = Event.objects.create(title='Test op',
                                    description='This is a test',
                                    owner=user,
                                    location='Salt River',
                                    state='published')
        i.province.add(province)
        i.save()

        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].event.location, 'Salt River')

        resp = self.client.get(reverse('events'))
        self.assertContains(resp, 'All (change)')
        self.assertContains(resp, 'Location: Salt River')

        resp = self.client.get(reverse('change_province'))
        self.assertEqual(resp.status_code, 200)

        url = '%s?next=/vlive/opportunities/events/' %\
                reverse('change_province', kwargs={'province': 1})
        resp = self.client.get(url)
        self.assertVLiveRedirects(resp, reverse('events'))

        resp = self.client.get(reverse('events'))
        self.assertContains(resp, 'Eastern Cape (change)')
        self.assertContains(resp, '0 events')

        url = '%s?next=/vlive/opportunities/events/' %\
                reverse('change_province', kwargs={'province': 3})
        resp = self.client.get(url)
        self.assertVLiveRedirects(resp, reverse('events'))

        resp = self.client.get(reverse('events'))
        self.assertContains(resp, 'Gauteng (change)')
        self.assertContains(resp, 'Location: Salt River')
