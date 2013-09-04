from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.core import mail

from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.vlive.utils import phone_number_to_international
import urllib

class VliveAuthenticationTestCase(VLiveTestCase):

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        settings.CELERY_ALWAYS_EAGER = True

    def tearDown(self):
        settings.CELERY_ALWAYS_EAGER = settings.DEBUG

    def test_index_page(self):
        self.client.login(username=self.msisdn, password=self.pin)
        resp = self.client.get(reverse('index'))
         #  there shouldn't be a Location header as this would mean a redirect
         #  to a login URL
        self.assertFalse(resp.get('Location', None))
        self.assertEquals(resp.status_code, 200)

    def test_login_view(self):
        resp = self.client.post(reverse('register'), {
            'username': self.msisdn,
            'new_password1': self.pin,
            'new_password2': self.pin,
        })
        self.assertContains(resp, 'Submitted successfully')

        resp = self.client.get(reverse('logout'))
        self.assertContains(resp, 'Submitted successfully')

        resp = self.client.get(reverse('login'), )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Enter PIN to sign in.')

        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
        })

        self.assertEquals(resp.status_code, 200)  # redirect to index
        self.assertContains(resp, 'Submitted successfully')

        resp = self.client.post(reverse('login'),{
            'password': 'wrong_pin',
        })

        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):

        resp = self.client.get(reverse('login'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'create a PIN')

        resp = self.client.get(reverse('register'))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Create PIN for %s' % (self.msisdn))

        resp = self.client.post(reverse('register'), {
            'username': self.msisdn,
            'new_password1': self.pin,
            'new_password2': self.pin,
        })

        # check that the PIN has been set and that we can now authenticate
        # with the ModelBackend using the msisdn and pin
        user = ModelBackend().authenticate(username=self.msisdn, password=self.pin)
        self.assertEqual(user.username, self.msisdn)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Submitted successfully')
        # ensure the session's pin has been set
        self.assertTrue(self.client.session[settings.UMMELI_PIN_SESSION_KEY])

        #test automatic login
        resp = self.client.get(reverse('profile'))
        self.assertContains(resp, 'My Profile')

        resp = self.client.get(reverse('logout'))
        self.assertContains(resp,  'Submitted successfully')
        # ensure the session's pin has been cleared
        self.assertNotIn(settings.UMMELI_PIN_SESSION_KEY, self.client.session)

        resp = self.client.get(reverse('login'))
        self.assertContains(resp, 'Enter PIN to sign in.')
        self.assertContains(resp, 'Forgot your PIN?')

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'

        resp = self.client.post(reverse('register'), {
            'username': msisdn,
            'password1': password,
            'password2': 'wrong',
        })
        self.assertContains(resp, 'PIN codes don&apos;t match.')

    def test_forgot_pin(self):

        #register user
        resp = self.client.post(reverse('register'),{
            'username': self.msisdn,
            'password1': self.pin,
            'password2': self.pin,
        })

        resp = self.client.get(reverse('forgot'))
        self.assertContains(resp, 'PIN will be sent to %s.' % self.msisdn)

        resp = self.client.post(reverse('forgot'),  {'username':self.msisdn})
        self.assertContains(resp, 'Submitted successfully')

    def test_change_pin(self):
        # register user
        resp = self.client.post(reverse('register'), {
            'username': self.msisdn,
            'new_password1': self.pin,
            'new_password2': self.pin,
        })
        self.assertContains(resp, 'Submitted successfully')

        # authorize with pin
        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
        })

        resp = self.client.get(reverse('password_change'))
        self.assertContains(resp, 'Change PIN for %s' % self.msisdn)

        resp = self.client.post(reverse('password_change'),{
            'old_password': self.pin,
           'new_password1': '5678',
           'new_password2': '5678',
        })
        self.assertContains(resp, 'Submitted successfully')

        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': '5678',
        })

        self.assertContains(resp, 'Submitted successfully')

    def test_phone_number_to_international(self):
        self.assertEquals(phone_number_to_international('0123456789'), '27123456789')
        self.assertEquals(phone_number_to_international('27123456789'), '27123456789')
        self.assertEquals(phone_number_to_international('271234567'), 'invalid no')
        self.assertEquals(phone_number_to_international('01234567'), 'invalid no')
        self.assertEquals(phone_number_to_international('username'), 'invalid no')

    def test_user_deactivated(self):
        self.register()
        user = User.objects.get(username=self.msisdn)
        user.is_active = False
        user.save()

        resp = self.client.post(reverse('login'), {
            'username': self.msisdn,
            'password': self.pin,
        })

        self.assertContains(resp, 'Your account has been deactivated')

        resp = self.client.get(reverse('contactsupport'))
        self.assertEquals(resp.status_code, 200)

        resp = self.client.post(reverse('contactsupport'), {
            'username': self.msisdn,
            'message': 'Im sorry I did this.',
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Blocked User: %s' % self.msisdn)
        self.assertEqual(mail.outbox[0].from_email, settings.SEND_FROM_EMAIL_ADDRESS)
        self.assertEqual(mail.outbox[0].to[0], settings.UMMELI_SUPPORT)

        #restore user status
        user.is_active = True
        user.save()
