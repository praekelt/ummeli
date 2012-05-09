from django.core.urlresolvers import reverse
from jmbocomments.test_utils import params_for_comments
from jmbocomments.models import UserComment
from jmboarticles.models import Article
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase


class CommentTestCase(VLiveTestCase):

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

    def place_comment(self, obj, **kwargs):
        params = params_for_comments(obj)
        params.update(kwargs)
        resp = self.client.post(reverse('comments-post-comment'),
            params)
        self.assertVLiveRedirects(resp, reverse('article_detail',
                                                args=[self.article.pk]))
        return UserComment.objects.latest('submit_date')

    def test_comment_paging(self):
        """Test pagination for comments"""
        for i in range(0, 20):
            self.place_comment(self.article, comment='hello world %s' % i,
            next=self.article_url)

        resp = self.client.get(reverse('article_detail_redo',
                                        args=[self.article.pk]))

        self.assertContains(resp, '20 comments')
        self.assertContains(resp, 'Next')
