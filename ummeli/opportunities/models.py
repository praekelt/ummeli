from django.db import models
from django.contrib.auth.models import User
from jmbo.models import ModelBase
from ummeli.base.models import PROVINCE_CHOICES


EDUCATION_LEVEL_CHOICES = (
        (0, 'Any'),
        (1, 'Matric or higher'),
        (2, 'Certificate or diploma'),
        (3, 'Degree'),
        (4, 'Post-graduate degree'),
        )

SALARY_FREQUENCY_CHOICES = (
        (1, 'day'),
        (7, 'week'),
        (31, 'month'),
        )


class Salary(models.Model):
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    frequency = models.PositiveIntegerField(
                    choices=SALARY_FREQUENCY_CHOICES,
                    default=1)

    def get_frequency(self):
        return dict(SALARY_FREQUENCY_CHOICES)[self.frequency]

    def __unicode__(self):  # pragma: no cover
        return '%s per %s' % (self.amount, self.get_frequency())


class Opportunity(ModelBase):
    province = models.PositiveIntegerField(choices=PROVINCE_CHOICES, default=0)
    deadline = models.DateTimeField(blank=True, null=True, default=None)
    education = models.PositiveIntegerField(
                    choices=EDUCATION_LEVEL_CHOICES,
                    default=0)
    salary = models.ForeignKey(Salary, blank=True, null=True, default=None)
    location = models.TextField(null=True, blank=True, default=None)

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('ummeli.opportunities.views.opportunity_detail', (self.slug,))

    class Meta:
        abstract = True


class Internship(Opportunity):
    pass


class Volunteer(Opportunity):
    pass


class Bursary(Opportunity):
    pass


class Training(Opportunity):
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class Competition(Opportunity):
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class Event(Opportunity):
    pass
