from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import (Internship, Salary, Training, Event,
                                            Province, MicroTask, Campaign)
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.contrib.sites.models import Site
from django.conf import settings


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
        web_site = Site(domain="web.address.com")
        web_site.save()
        settings.SITE_ID = web_site.id

        t1 = MicroTask(title='Test1', state='published')
        t1.save()
        t1.sites.add(web_site)

        t2 = MicroTask(title='Test2', users_per_task=0, state='published')
        t2.save()
        t2.sites.add(web_site)

        t3 = MicroTask(title='Test3', users_per_task=2, state='published')
        t3.save()
        t3.sites.add(web_site)

        t4 = MicroTask(title='Test4', users_per_task=2, state='published')
        t4.save()
        t4.sites.add(web_site)

        self.assertEqual(MicroTask.permitted.all().count(), 4)
        self.assertEqual(MicroTask.available.all().count(), 4)

        user = User.objects.get(username=self.msisdn)
        user2 = User.objects.get(username='27121111111')

        #simple case - 1 user per task
        self.assertTrue(t1.is_available())
        result = t1.checkout(user)
        self.assertTrue(result)
        self.assertFalse(t1.is_available())
        self.assertEqual(MicroTask.available.all().count(), 3)

        #infinite checkouts available
        self.assertTrue(t2.is_available())
        result = t2.checkout(user)
        self.assertTrue(result)
        self.assertTrue(t2.is_available())
        self.assertEqual(MicroTask.available.all().count(), 3)

        #custom - 2 users per task
        self.assertTrue(t3.is_available())
        result = t3.checkout(user)
        self.assertTrue(result)
        self.assertTrue(t3.is_available())
        result = t3.checkout(user2)
        self.assertTrue(result)
        self.assertFalse(t3.is_available())
        self.assertEqual(MicroTask.available.all().count(), 2)

        #negative case - user attempt to checkout a task twice
        self.assertTrue(t4.is_available())
        result = t4.checkout(user)
        self.assertTrue(result)
        self.assertTrue(t4.is_available())
        result = t4.checkout(user)
        self.assertFalse(result)
        self.assertTrue(t4.is_available())

    def test_task_expiration(self):
        user = User.objects.get(username=self.msisdn)

        web_site = Site(domain="web.address.com")
        web_site.save()
        settings.SITE_ID = web_site.id

        t1 = MicroTask(title='task1', state='published')
        t1.save()
        t1.sites.add(web_site)

        t2 = MicroTask(title='task2', state='published')
        t2.save()
        t2.sites.add(web_site)

        c = Campaign.objects.create(title='Campaign1')
        c.tasks.add(t1)
        c.tasks.add(t2)

        self.assertTrue(t1.is_available())

        d1 = datetime.now() - timedelta(hours=16)
        t1.checkout(user)
        t_checkout = t1.taskcheckout_set.all()[0]
        t_checkout.date = d1
        t_checkout.save()

        MicroTask.expire_tasks()
        self.assertFalse(t1.is_available())

        self.assertTrue(t2.is_available())

        d1 = datetime.now() - timedelta(hours=25)
        t2.checkout(user)
        t_checkout = t2.taskcheckout_set.all()[0]
        t_checkout.date = d1
        t_checkout.save()

        MicroTask.expire_tasks()
        self.assertTrue(t2.is_available())

        self.assertEqual(Campaign.available_tasks().count(), 1)
