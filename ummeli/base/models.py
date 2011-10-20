from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.conf import settings

from ummeli.base import email_copy
from ummeli.base.utils import render_to_pdf
from django.core.mail import send_mail,  EmailMessage

class Certificate (models.Model):
    name = models.CharField(max_length=45)
    institution = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(default=0, null=True, blank=True)
    
    def __unicode__(self):  # pragma: no cover
        return self.name + " @ " + self.institution
        
class Language (models.Model):
    language = models.CharField(max_length=45)
    readWrite = models.BooleanField(default=False)
    
    def __unicode__(self):  # pragma: no cover
        return self.language
        
class WorkExperience (models.Model):
    title = models.CharField(max_length=45)
    company = models.CharField(max_length=45, null=True, blank=True)
    startYear = models.IntegerField(default=0, null=True, blank=True)
    endYear = models.IntegerField(default=0, null=True, blank=True)
    
    def __unicode__(self):  # pragma: no cover
        return self.title + " @ " + self.company
        
class Reference (models.Model):
    fullname = models.CharField(max_length=45)
    relationship = models.CharField(max_length=45, null=True, blank=True)
    contactNo = models.CharField(max_length=45, null=True, blank=True)
    
    def __unicode__(self):  # pragma: no cover
        return self.fullname

class CurriculumVitae(models.Model):
    firstName = models.CharField(max_length=45, null=True, blank=True)
    surname = models.CharField(max_length=45, null=True, blank=True)
    gender = models.CharField(max_length=45, null=True, blank=True)
    email = models.CharField(max_length=45, null=True, blank=True)
    telephoneNumber = models.CharField(max_length=45, null=True, blank=True)
    location = models.CharField(max_length=45, null=True, blank=True)
    streetName = models.CharField(max_length=45, null=True, blank=True)
    school = models.CharField(max_length=45, null=True, blank=True)
    highestGrade = models.CharField(max_length=45, null=True, blank=True)
    highestGradeYear = models.IntegerField(default=0, null=True, blank=True)
    dateOfBirth = models.CharField(max_length=45, null=True, blank=True)
    houseNumber = models.CharField(max_length=45, null=True, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    workExperiences = models.ManyToManyField(WorkExperience, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    user = models.OneToOneField('auth.User')
    nr_of_faxes_sent = models.IntegerField(default=0,  editable=False)
    
    def fullname(self):
        return '%s %s' % (self.firstName,  self.surname)
    
    def can_send_fax(self):
        return self.nr_of_faxes_sent < settings.MAX_LAUNCH_FAXES_COUNT
        
    def fax_cv(self,  fax_nr, article_text = None):
        if(self.can_send_fax()):
            self.nr_of_faxes_sent += 1
            self.save()
            return self.email_cv('%s@faxfx.net' % fax_nr.replace(' ', ''),  article_text)
        return None
        
    def email_cv(self, email_address, article_text = None):
        email_text = ''
        if article_text:
            email_text = email_copy.APPLY_COPY % {'sender': self.fullname(), 
                                                                            'job_ad':article_text}
        else:
            email_text = email_copy.SEND_COPY % {'sender': self.fullname(), 
                                                                           'job_ad':article_text}
            
        email = EmailMessage('CV for %s' % self.fullname(), email_text, 
                                            'no-reply@ummeli.org',
                                            [email_address])
        pdf = render_to_pdf('pdf_template.html', {'model': self})
        email.attach('curriculum_vitae_for_%s_%s' % (self.firstName, self.surname), 
                            pdf,  'application/pdf')
        return email.send(fail_silently=False)
        
    def __unicode__(self):  # pragma: no cover
        return u"CurriculumVitae %s - %s" % (self.pk, self.firstName)

class CurriculumVitaeForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        exclude = ('user')
        
def create_cv(sender, instance, created, **kwargs):
    if created:
        cv = CurriculumVitae.objects.create(firstName=instance.first_name, 
                surname=instance.last_name, email=instance.email,
                user=instance)

post_save.connect(create_cv, sender = User, 
                  dispatch_uid = "users-profilecreation-signal")
