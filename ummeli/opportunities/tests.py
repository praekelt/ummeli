from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import (Internship, Salary, Training, Event,
                                            Province, MicroTask, Campaign)
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta


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

    def test_province_from_str(self):
        p = Province.from_str('Gauteng')
        self.assertEqual(p.pk, 3)

        p = Province.from_str('KwaZulu Natal')
        self.assertEqual(p.pk, 4)
        p = Province.from_str('Kwa-Zulu Natal')
        self.assertEqual(p.pk, 4)

        p = Province.from_str('Western Cape')
        self.assertEqual(p.pk, 9)

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
                                    place='Salt River')
        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].event.place, 'Salt River')

    def test_change_province_session(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)
        province = Province.objects.get(province=3)
        i = Event.objects.create(title='Test op',
                                    description='This is a test',
                                    owner=user,
                                    place='Salt River',
                                    state='published')
        i.province.add(province)
        i.save()

        self.assertEqual(user.modelbase_set.filter(slug=i.slug).count(), 1)
        self.assertEqual(user.modelbase_set.all()[0].event.place, 'Salt River')

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

    def test_task_checkout(self):
        t1 = MicroTask(title='Test1')
        t1.save()
        t2 = MicroTask(title='Test2', users_per_task=0)
        t2.save()
        t3 = MicroTask(title='Test3', users_per_task=2)
        t3.save()
        t4 = MicroTask(title='Test4', users_per_task=2)
        t4.save()

        user = User.objects.get(username=self.msisdn)
        user2 = User.objects.get(username='27121111111')

        #simple case - 1 user per task
        self.assertTrue(t1.available())
        result = t1.checkout(user)
        self.assertTrue(result)
        self.assertFalse(t1.available())

        #infinite checkouts available
        self.assertTrue(t2.available())
        result = t2.checkout(user)
        self.assertTrue(result)
        self.assertTrue(t2.available())

        #custom - 2 users per task
        self.assertTrue(t3.available())
        result = t3.checkout(user)
        self.assertTrue(result)
        self.assertTrue(t3.available())
        result = t3.checkout(user2)
        self.assertTrue(result)
        self.assertFalse(t3.available())

        #negative case - user attempt to checkout a task twice
        self.assertTrue(t4.available())
        result = t4.checkout(user)
        self.assertTrue(result)
        self.assertTrue(t4.available())
        result = t4.checkout(user)
        self.assertFalse(result)
        self.assertTrue(t4.available())

    def test_task_expiration(self):
        user = User.objects.get(username=self.msisdn)

        t1 = MicroTask(title='task1')
        t1.save()
        t2 = MicroTask(title='task2')
        t2.save()

        c = Campaign.objects.create(title='Campaign1')
        c.tasks.add(t1)
        c.tasks.add(t2)

        self.assertTrue(t1.available())

        d1 = datetime.now() - timedelta(hours=16)
        t1.checkout(user)
        t_checkout = t1.taskcheckout_set.all()[0]
        t_checkout.date = d1
        t_checkout.save()

        MicroTask.expire_tasks()
        self.assertFalse(t1.available())

        self.assertTrue(t2.available())

        d1 = datetime.now() - timedelta(hours=25)
        t2.checkout(user)
        t_checkout = t2.taskcheckout_set.all()[0]
        t_checkout.date = d1
        t_checkout.save()

        MicroTask.expire_tasks()
        self.assertTrue(t2.available())

        self.assertEqual(Campaign.available_tasks().count(), 1)
