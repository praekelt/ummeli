from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from jmbo.models import ModelBase
from ummeli.base.models import PROVINCE_CHOICES
from ummeli.vlive.templatetags.vlive_tags import sanitize_html
from datetime import datetime, timedelta, date
from django.db.models import Q, F, Count
from jmbo.managers import PermittedManager
import re


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

    @classmethod
    def from_str(cls, str):
        result = [i for i, p in PROVINCE_CHOICES
                    if re.sub('[\s-]', '', p.lower()) ==
                        re.sub('[\s-]', '', str.lower())]

        if len(result) > 1:
            raise MultipleObjectsReturned

        if any(result):
            return cls.objects.get(pk=result[0])
        return None


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

    def as_leaf_class(self):
        try:
            instance = self.__getattribute__(self.class_name.lower())
        except AttributeError:
            content_type = self.content_type
            model = content_type.model_class()
            if(model == ModelBase):
                return self
            instance = model.objects.get(id=self.id)
        return instance

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


class AvailableManager(PermittedManager):
    use_for_related_fields = False

    def get_query_set(self):
        # Get base queryset and exclude based on state.
        queryset = super(AvailableManager, self).get_query_set()\
                        .filter(Q(taskcheckout__state__lt=EXPIRED) |
                                Q(taskcheckout__isnull=True))\
                        .annotate(checkedout_tasks=Count('taskcheckout'))\
                        .filter(Q(checkedout_tasks__lt=F('users_per_task')) |
                                Q(users_per_task=0))
        return queryset


class Campaign(Opportunity):
    must_qualify = models.BooleanField(default=False)
    qualifiers = models.ManyToManyField(User, blank=True, null=True)
    qualification_instructions = models.TextField(blank=True, null=True)

    def has_qualified(self, user):
        if not self.must_qualify:
            return True

        return self.qualifiers.filter(id=user.id)

    @models.permalink
    def get_absolute_url(self):
        return ('campaign_detail', (self.slug,))

    def get_template(self):
        return 'opportunities/microtasks/campaign_detail_default.html'

    @classmethod
    def available_tasks(cls):
        return cls.objects.filter(Q(tasks__taskcheckout__state=EXPIRED) |
                                    Q(tasks__taskcheckout__isnull=True))

    def tasks_new(self):
        return self.tasks.filter(created__gte=date.today())

    def responses(self):
        return self.tasks.filter(microtaskresponse__state=SUBMITTED)\
                        .order_by('microtaskresponse__date')

    def responses_new(self):
        return self.tasks.filter(microtaskresponse__state=SUBMITTED,
                                microtaskresponse__date__gte=date.today())

    def accepted(self):
        return self.tasks.filter(microtaskresponse__state=ACCEPTED)\
                        .order_by('microtaskresponse__date')

    def rejected(self):
        return self.tasks.filter(microtaskresponse__state=REJECTED)\
                        .order_by('microtaskresponse__date')


class TomTomCampaign(Campaign):
    def get_template(self):
        return 'opportunities/tomtom/campaign_detail.html'


class MicroTask(Opportunity):
    objects = models.Manager()
    available = AvailableManager()
    campaign = models.ForeignKey(Campaign, related_name='tasks')
    users_per_task = models.PositiveIntegerField(default=1)
    hours_per_task = models.PositiveIntegerField(default=24)

    @models.permalink
    def get_absolute_url(self):
        return ('micro_task_detail', (self.slug,))

    def is_available(self):
        return self.users_per_task == 0 or\
            self.taskcheckout_set.filter(state__lt=EXPIRED).count() < self.users_per_task

    def available_for(self, user):
        if self.taskcheckout_set.filter(state__lt=EXPIRED, user=user).exists():
            return False
        return self.is_available()

    def checked_out_by(self, user):
        return self.taskcheckout_set.filter(state__lte=RETURNED, user=user).exists()

    def checkout(self, user):
        if self.available_for(user):
            task = TaskCheckout(user=user, task=self)
            task.save()
            return True
        return False

    @classmethod
    def expire_tasks(cls):
        for task in cls.permitted.all():
            if task.hours_per_task == 0:  # no limit
                continue

            cutoff_date = datetime.now() - timedelta(hours=task.hours_per_task)
            task.taskcheckout_set.filter(task=task, state=OPEN,
                                        date__lte=cutoff_date)\
                                .update(state=EXPIRED)


OPEN = 0
RETURNED = 1
EXPIRED = 2

TASK_CHECKOUT_STATE = (
    (OPEN, 'Open'),
    (RETURNED, 'Returned'),
    (EXPIRED, 'Expired'),
    )


class TaskCheckout(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(MicroTask)
    state = models.PositiveIntegerField(choices=TASK_CHECKOUT_STATE,
                                        default=OPEN)
    date = models.DateTimeField(auto_now_add=True)

    def expires_on(self):
        return self.date + timedelta(hours=self.task.hours_per_task)


class TomTomMicroTask(MicroTask):
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

SUBMITTED = 0
ACCEPTED = 1
REJECTED = 2

TASK_RESPONSE_STATE = (
    (SUBMITTED, 'Submitted'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    )


class MicroTaskResponse(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(MicroTask)
    task_checkout = models.OneToOneField(TaskCheckout)
    state = models.PositiveIntegerField(choices=TASK_RESPONSE_STATE,
                                        default=SUBMITTED)
    date = models.DateTimeField(auto_now_add=True)


class TomTomMicroTaskResponse(MicroTaskResponse):
    file = models.ImageField(upload_to='microtask_uploads/', blank=False, null=False)
    tel_1 = models.TextField(blank=True, null=True)
    tel_2 = models.TextField(blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    poi_has_changed = models.BooleanField(default=False)
