from django.core.urlresolvers import reverse
from jmbocomments.test_utils import params_for_comments
from jmbocomments.models import UserComment
from jmboarticles.models import Article
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.vlive.tasks import enable_commenting, disable_commenting


class ArticlesTestCase(VLiveTestCase):

    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
        'vlive/tests/article/fixtures/sample.json',
    ]

    def setUp(self):
        self.article = Article.published_objects.latest()
        self.article_url = reverse('article_detail', kwargs={
            'pk': self.article.pk,
        })

        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)
        self.client.login(remote_user=self.msisdn)

    def test_commenting_open(self):
        """Test closing comments"""
        pk = self.article.pk
        resp = self.client.get(reverse('article_detail_redo', args=[pk]))
        self.assertNotContains(resp, 'Comments are closed')

        disable_commenting()

        resp = self.client.get(reverse('article_detail_redo', args=[pk]))
        self.assertContains(resp, 'Comments are closed')

        enable_commenting()

        resp = self.client.get(reverse('article_detail_redo', args=[pk]))
        self.assertNotContains(resp, 'Comments are closed')

        enable_commenting()

        resp = self.client.get(reverse('article_detail_redo', args=[pk]))
        self.assertNotContains(resp, 'Comments are closed')
