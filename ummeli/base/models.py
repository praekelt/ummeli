from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.conf import settings
from django.template.loader import render_to_string

from ummeli.base.utils import render_to_pdf
from django.core.mail import send_mail,  EmailMessage
from datetime import datetime

from celery.task import task

class Article(models.Model):
    hash_key = models.CharField(max_length=32, unique=True)
    date = models.DateTimeField(blank=True,  default = datetime.now())
    source = models.CharField(max_length=100)
    text = models.TextField()

    def __unicode__(self):  # pragma: no cover
        return '%s - %s - %s' % (self.date,  self.source,  self.text)
    
    def user_submitted(self):
                return 0


class UserSubmittedJobArticle(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(default='')
    moderated = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name='user_submitted_job_article_user')

    def __unicode__(self):  # pragma: no cover
        return '%s - %s - %s - %s' % (self.date, self.user.username, self.title, self.text)
    
    def user_submitted(self):
                return 1

    def to_view_model(self):
        class UserSubmittedJobArticleViewModel(object):
            def __init__(self,  user_article):
                self.pk = user_article.pk
                self.source = user_article.title
                self.text = user_article.text
                self.date = user_article.date
                self.user = user_article.user
                
            def user_submitted(self):
                return 1
        return UserSubmittedJobArticleViewModel(self)


class Province(models.Model):
    search_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=45)

    def __unicode__(self):  # pragma: no cover
        return self.name


class Category(models.Model):
    hash_key = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=45)
    province = models.ForeignKey(Province)
    articles = models.ManyToManyField(Article, blank=True,  null=True)
    user_submitted_job_articles = models.ManyToManyField(UserSubmittedJobArticle, blank=True,  null=True)

    def must_show(self):
        return self.articles.exists() or self.user_submitted_job_articles.exists()
    
    def articles_count(self):
        return self.articles.count() + self.user_submitted_job_articles.count()

    def __unicode__(self):  # pragma: no cover
        return '%s - %s (%s)' % (self.province.name, self.title, self.articles_count())


class Certificate (models.Model):
    name = models.CharField(max_length=45)
    institution = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):  # pragma: no cover
        return self.name + " @ " + self.institution

class Language (models.Model):
    language = models.CharField(max_length=45)
    read_write = models.BooleanField(default=False)

    def __unicode__(self):  # pragma: no cover
        return self.language

class WorkExperience (models.Model):
    title = models.CharField(max_length=45)
    company = models.CharField(max_length=45, null=True, blank=True)
    start_year = models.IntegerField(default=0, null=True, blank=True)
    end_year = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):  # pragma: no cover
        return self.title + " @ " + self.company

class Reference (models.Model):
    fullname = models.CharField(max_length=45)
    relationship = models.CharField(max_length=45, null=True, blank=True)
    contact_no = models.CharField(max_length=45, null=True, blank=True)

    def __unicode__(self):  # pragma: no cover
        return self.fullname
    
    
class Skill (models.Model):
    skill = models.CharField(max_length=45, null=False, blank=False)


class CurriculumVitae(models.Model):
    first_name = models.CharField(max_length=45, null=True, blank=True)
    surname = models.CharField(max_length=45, null=True, blank=True)
    gender = models.CharField(max_length=45, null=True, blank=True)
    email = models.CharField(max_length=45, null=True, blank=True)
    telephone_number = models.CharField(max_length=45, null=True, blank=True)
    location = models.CharField(max_length=45, null=True, blank=True)
    street_name = models.CharField(max_length=45, null=True, blank=True)
    school = models.CharField(max_length=45, null=True, blank=True)
    highest_grade = models.CharField(max_length=45, null=True, blank=True)
    highest_grade_year = models.IntegerField(default=0, null=True, blank=True)
    date_of_birth = models.CharField(max_length=45, null=True, blank=True)
    house_number = models.CharField(max_length=45, null=True, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    work_experiences = models.ManyToManyField(WorkExperience, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    user = models.OneToOneField('auth.User')
    nr_of_faxes_sent = models.IntegerField(default=0,  editable=False)
    is_complete = models.BooleanField(default=False,  editable=False)
    
    preferred_skill = models.ForeignKey(Skill, blank=True, null=True, related_name='profiles_preferred')
    skills = models.ManyToManyField(Skill, blank=True, null=True, related_name='profiles')

    connection_requests = models.ManyToManyField('auth.User', related_name='connection_requests', blank=True)
    
    def is_connection_requested(self, user_id):
        return self.connection_requests.filter(pk=user_id).exists()
    
    def __str__(self):
        return '%s - %s %s' % (self.user.username, self.first_name,  self.surname)
    
    def fullname(self):
        return '%s %s' % (self.first_name,  self.surname)

    def missing_fields(self):
        fields = []
        if not self.first_name:
            fields.append('first name')
        if not self.surname:
            fields.append('surname')
        if not self.gender:
            fields.append('gender')
        if not self.telephone_number:
            fields.append('telephone number')
        if not self.date_of_birth:
            fields.append('date of birth')
        if not self.highest_grade:
            fields.append('highest grade passed')
        if not self.languages.exists():
            fields.append('atleast 1 language')
        return fields
    
    def fields_complete(self):
        count = 0.0
        if  self.first_name:
            count += 1
        if  self.surname:
            count += 1
        if  self.gender:
            count += 1
        if  self.email:
            count += 1
        if  self.telephone_number:
            count += 1
        if  self.location:
            count += 1
        if  self.street_name:
            count += 1
        if  self.school:
            count += 1
        if  self.highest_grade:
            count += 1
        if  self.highest_grade_year:
            count += 1
        if  self.date_of_birth:
            count += 1
        if  self.house_number:
            count += 1
        if  self.certificates.exists():
            count += 1
        if  self.languages.exists():
            count += 1
        if  self.work_experiences.exists():
            count += 1
        if  self.references.exists():
            count += 1
        return (count/16)*100

    def update_is_complete(self):
        if not self.missing_fields():
            self.is_complete = True
        else:
            self.is_complete = False
        self.save()

    def can_send_fax(self):
        return self.nr_of_faxes_sent < settings.MAX_LAUNCH_FAXES_COUNT

    def faxes_remaining(self):
        return settings.MAX_LAUNCH_FAXES_COUNT - self.nr_of_faxes_sent

    def fax_cv(self,  fax_nr, article_text = None):
        if(self.can_send_fax()):
            self.nr_of_faxes_sent += 1
            self.save()
            return self.email_cv('%s@faxfx.net' % fax_nr.replace(' ', ''),
                                 article_text, settings.SEND_FROM_FAX_EMAIL_ADDRESS)
        return None

    def email_cv(self, email_address, article_text = None,
                        from_address = settings.SEND_FROM_EMAIL_ADDRESS):
        email_text = ''
        copy_context = {'sender': self.fullname(), 
                                'job_ad': article_text, 
                                'phone': self.telephone_number}
        
        if article_text:
            email_text = render_to_string('apply_copy.txt', copy_context)
        else:
            email_text = render_to_string('send_copy.txt', copy_context)

        schedule_cv_email.delay(self,  email_address,  email_text,  from_address)

    def __unicode__(self):  # pragma: no cover
        return u"CurriculumVitae %s - %s" % (self.pk, self.first_name)

def update_is_complete_property(sender, **kwargs):
    instance = kwargs['instance']
    # Use a list operation, prevents the signal to be fired again
    # when it is being updated for the `is_complete` boolean.
    CurriculumVitae.objects.filter(pk=instance.pk).update(
        is_complete=not instance.missing_fields())

post_save.connect(update_is_complete_property, sender=CurriculumVitae,
    dispatch_uid='curriculum-vitae-is-complete-signal')

class CurriculumVitaeForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        exclude = ('user')

def create_cv(sender, instance, created, **kwargs):
    if created:
        cv = CurriculumVitae.objects.create(first_name=instance.first_name,
                surname=instance.last_name, email=instance.email,
                user=instance)

post_save.connect(create_cv, sender = User,
                  dispatch_uid = "users-profilecreation-signal")

@task
def schedule_cv_email(cv,  email_address,  email_text, from_address):
    email = EmailMessage('CV for %s' % cv.fullname(), email_text,
                                            from_address,
                                            [email_address], ['ummeli@praekeltfoundation.org'])
    pdf = render_to_pdf('pdf_template.html', {'model': cv})
    email.attach('curriculum_vitae_for_%s_%s.pdf' % (cv.first_name, cv.surname),
                        pdf,  'application/pdf')
    email.send(fail_silently=False)
