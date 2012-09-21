from django.db import models
from django.contrib.auth.models import User
from jmbo.models import ModelBase
from ummeli.base.models import PROVINCE_CHOICES
from ummeli.vlive.templatetags.vlive_tags import sanitize_html

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


class Province(models.Model):
    province = models.PositiveIntegerField(choices=PROVINCE_CHOICES, default=0)

    def __unicode__(self):  # pragma: no cover
        return '%s' % dict(PROVINCE_CHOICES)[self.province]


class Salary(models.Model):
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    frequency = models.PositiveIntegerField(
                    choices=SALARY_FREQUENCY_CHOICES,
                    default=1)

    def get_frequency(self):
        return dict(SALARY_FREQUENCY_CHOICES)[self.frequency]

    def __unicode__(self):  # pragma: no cover
        return '%s per %s' % (self.amount, self.get_frequency())

    class Meta:
        verbose_name_plural = "salaries"


class Opportunity(ModelBase):
    province = models.ManyToManyField(
                    Province,
                    blank=True,
                    null=True,
                    default=None)
    education = models.PositiveIntegerField(
                    choices=EDUCATION_LEVEL_CHOICES,
                    default=0)
    salary = models.ForeignKey(Salary, blank=True, null=True, default=None)
    place = models.TextField(null=True, blank=True, default=None)

    def __unicode__(self):  # pragma: no cover
        return '%s' % self.title

    def get_education(self):
        return dict(EDUCATION_LEVEL_CHOICES)[self.education]

    def get_provinces(self):
        print self.province.all()
        return ', '.join(['%s' % a for a in self.province.all()])

    def save(self, *args, **kwargs):
        self.description = sanitize_html(self.description or '')
        self.place = sanitize_html(self.place or '')
        super(Opportunity, self).save(*args, **kwargs)

    class Meta:
        abstract = True

Opportunity._meta.get_field_by_name('sites')[0].blank = False


class Job(Opportunity):
    @models.permalink
    def get_absolute_url(self):
        return ('job_opportunity', (self.slug,))


class Internship(Opportunity):
    @models.permalink
    def get_absolute_url(self):
        return ('internship_detail', (self.slug,))


class Volunteer(Opportunity):
    @models.permalink
    def get_absolute_url(self):
        return ('volunteer_detail', (self.slug,))

    class Meta:
        verbose_name_plural = "volunteering"


class Bursary(Opportunity):
    @models.permalink
    def get_absolute_url(self):
        return ('bursary_detail', (self.slug,))

    class Meta:
        verbose_name_plural = "bursaries"


class Training(Opportunity):
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    @models.permalink
    def get_absolute_url(self):
        return ('training_detail', (self.slug,))

    class Meta:
        verbose_name_plural = "training"


class Competition(Opportunity):
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    @models.permalink
    def get_absolute_url(self):
        return ('competition_detail', (self.slug,))


class Event(Opportunity):
    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', (self.slug,))


class MicroTask(Opportunity):
    @models.permalink
    def get_absolute_url(self):
        return ('micro_task_detail', (self.slug,))


class TomTomMicroTask(MicroTask):
    @models.permalink
    def get_absolute_url(self):
        return ('tom_tom_micro_task_detail', (self.slug,))

    category = models.TextField(blank=True, null=True)
    poi_id = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)
    tel_1 = models.TextField(blank=True, null=True)
    tel_2 = models.TextField(blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)

    def to_dto(self):
        return {'title': self.title,
                'description': self.description,
                'published': self.state == 'published',
                'x_coordinate': '%s' % self.location.coordinates[0],
                'y_coordinate': '%s' % self.location.coordinates[1],
                'category': self.category,
                'tel_1': self.tel_1,
                'tel_2': self.tel_2,
                'fax': self.fax,
                'email': self.email,
                'website': self.website,
                'poi_id': self.poi_id,
                'id': self.id,
                }


class Campaign(Opportunity):
    tasks = models.ManyToManyField(MicroTask,
                    blank=True,
                    null=True,
                    default=None)
    must_qualify = models.BooleanField(default=False)
    qualifiers = models.ManyToManyField(User, blank=True, null=True)
    qualification_instructions = models.TextField(blank=True, null=True)

    def has_qualified(self, user):
        return self.qualifiers.filter(pk=user.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('campaign_detail', (self.slug,))
