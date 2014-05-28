from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from ummeli.base.utils import render_to_pdf


class BaseTestCase(TestCase):
    fixtures = [
        'fixtures/opportunities.provinces.json',
    ]

    def setUp(self):
        self.client = Client()
        username = '0123456789'
        password = 'password'
        self.user = User.objects.create_user(
            username, '%s@domain.com' % username,
            password)
        self.client.login(username=username, password=password)

    def tearDown(self):
        pass

    def test_convert_to_pdf(self):
        cv = self.user.get_profile()
        result = render_to_pdf('pdf_template.html', {'model': cv})
        self.assertNotEquals(result, None)

    def test_apply_copy(self):
        copy_context = {
            'sender': 'Joe Soap',
            'job_ad': 'This is a sample job ad.',
            'phone': '0123456789',
            'message': 'How I love to work!',
            'date': datetime(2014, 5, 12)}

        text = render_to_string('apply_copy.txt', copy_context)
        self.assertTrue('My name is Joe Soap' in text)
        self.assertTrue('contact me directly on 0123456789' in text)
        self.assertTrue('position you advertised on 2014-05-12' in text)
