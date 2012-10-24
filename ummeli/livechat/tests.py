from django.test import TestCase
from django.test.client import Client
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from jmbocomments.test_utils import params_for_comments
from jmbocomments.models import UserComment
from ummeli.livechat.models import LiveChat


current_site = Site.objects.get_current()


class LiveChatTestCase(TestCase):

    fixtures = [
        'auth/fixtures/sample-data.json',
    ]

    def setUp(self):
        self.msisdn = '1234567890'
        self.client = Client(HTTP_VTL_USER_MSISDN=self.msisdn)
        self.livechat = LiveChat.objects.create(title='live chat',
                                                description='live chat')
        self.livechat.sites.add(current_site)
        self.livechat.save()

        self.livechat_url = reverse('livechat:show', kwargs={
            'pk': self.livechat.pk,
        })

        self.comment = self.place_comment(self.livechat,
            comment='hello live chat', next=self.livechat_url)

    def place_comment(self, obj, **kwargs):
        params = params_for_comments(obj)
        params.update(kwargs)
        response = self.client.post(reverse('comments-post-comment'),
            params)
        self.assertEqual(response.status_code, 302)
        return UserComment.objects.latest('submit_date')

    def tearDown(self):
        pass

    def test_logged_in_required(self):
        client = Client()
        response = client.get(self.livechat_url)
        self.assertNotContains(response, 'Write your question')
        self.assertContains(response, self.comment.comment)
        authed_response = client.get(self.livechat_url,
            HTTP_VTL_USER_MSISDN=self.msisdn)
        self.assertContains(authed_response, 'Write your question')
        self.assertContains(response, self.comment.comment)

    def test_active_livechat(self):
        response = self.client.get(self.livechat_url)
        self.assertContains(response, 'Write your question')
        self.assertContains(response, self.comment.comment)

    def test_inactive_livechat(self):
        self.livechat.active = False
        self.livechat.save()

        response = self.client.get(self.livechat_url)
        self.assertNotContains(response, 'Write your question')
        self.assertContains(response, self.comment.comment)
