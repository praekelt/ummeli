from django.db import models
from django.contrib.auth.models import User
from jmbo.models import ModelBase


class Opportunity(ModelBase):
    province = models.IntegerField(default=0)
    deadline = models.DateTimeField(blank=True, null=True, default=None)
    provider = models.ForeignKey(User)

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.title
