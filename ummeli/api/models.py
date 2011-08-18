from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms import ModelForm

class Certificate (models.Model):
    name = models.CharField(max_length=45)
    institution = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(default=0, null=True, blank=True)
    def __unicode__(self): # pragma: no cover
        return self.name + " @ "+ self.institution
        
class Language (models.Model):
    language = models.CharField(max_length=45)
    readWrite = models.IntegerField(default=0)
    def __unicode__(self): # pragma: no cover
        return self.language
        
class WorkExperience (models.Model):
    title = models.CharField(max_length=45)
    company = models.CharField(max_length=45, null=True, blank=True)
    startYear = models.IntegerField(default=0, null=True, blank=True)
    endYear = models.IntegerField(default=0, null=True, blank=True)
    def __unicode__(self): # pragma: no cover
        return self.title + " @ "+ self.company
        
class Reference (models.Model):
    fullname = models.CharField(max_length=45)
    relationship = models.CharField(max_length=45, null=True, blank=True)
    contactNo = models.CharField(max_length=45, null=True, blank=True)
    def __unicode__(self): # pragma: no cover
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

    def __unicode__(self): # pragma: no cover
        return u"CurriculumVitae %s - %s" % (self.pk, self.firstName)

class CurriculumVitaeForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        exclude = ('user')
        
class PersonalDetailsForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        exclude = ('user', 'references', 'workExperiences', 'languages',
                'certificates')

def create_cv(sender, instance, created, **kwargs):
    if created:
        cv = CurriculumVitae.objects.create(firstName=instance.first_name, 
                surname=instance.last_name, email=instance.email,
                user=instance)
        
    else:
        cv = instance.get_profile()
        cv.firstName = instance.first_name
        cv.surname = instance.last_name
        cv.email = instance.email
        cv.save()

post_save.connect(create_cv, sender=User, dispatch_uid="users-profilecreation-signal")
