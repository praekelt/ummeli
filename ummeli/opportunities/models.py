from django.db import models
from django.contrib.auth.models import User
from jmbo.models import ModelBase
from ummeli.base.models import PROVINCE_CHOICES


class Opportunity(ModelBase):
    province = models.PositiveIntegerField(choices=PROVINCE_CHOICES, default=0)
    deadline = models.DateTimeField(blank=True, null=True, default=None)
    provider = models.ForeignKey(User)

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.title

    class Meta:
        abstract = True


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


class Internship(Opportunity):
    education = models.PositiveIntegerField(
                    choices=EDUCATION_LEVEL_CHOICES,
                    default=0)
    salary = models.ForeignKey(Salary)

    @models.permalink
    def get_absolute_url(self):
        return ('ummeli.opportunities.views.internship_detail', (self.slug,))
