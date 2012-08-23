from django.db import models
from django.contrib.auth.models import User
from jmbo.models import ModelBase
from ummeli.base.models import PROVINCE_CHOICES


class Opportunity(ModelBase):
    province = models.PositiveIntegerField(choices=PROVINCE_CHOICES, default=0)
    deadline = models.DateTimeField(blank=True, null=True, default=None)
    provider = models.ForeignKey(User)

    @models.permalink
    def get_absolute_url(self):
        return ('ummeli.opportunities.views.detail', (self.slug,))

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.title
