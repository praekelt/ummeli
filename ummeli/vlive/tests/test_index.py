from django.core.urlresolvers import reverse
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from jmboyourwords.management.commands.your_words_content_scheduler\
    import Command


class VLiveIndexTestCase(VLiveTestCase):
    fixtures = [
        'vlive/tests/yourwords/fixtures/sample.json',
        'vlive/tests/auth/fixtures/sample.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        self.client.login(remote_user=self.msisdn)

    def test_index_page(self):
        c = Command()
        c.publish()
        
        resp = self.client.get(reverse('index'))
        self.assertContains(resp, 'Another competition')
        self.assertContains(resp, 'Where are you')
