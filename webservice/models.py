from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Certificate (models.Model):
    name = models.CharField(max_length=45)
    institution = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(default=0, null=True, blank=True)
    def __unicode__(self):
        return self.name + " @ "+ self.institution
        
class Language (models.Model):
    language = models.CharField(max_length=45)
    readwrite = models.IntegerField(default=0)
    def __unicode__(self):
        return self.language
        
class Workexperience (models.Model):
    title = models.CharField(max_length=45)
    company = models.CharField(max_length=45, null=True, blank=True)
    startyear = models.IntegerField(default=0, null=True, blank=True)
    endyear = models.IntegerField(default=0, null=True, blank=True)
    def __unicode__(self):
        return self.title + " @ "+ self.company
        
class Reference (models.Model):
    fullname = models.CharField(max_length=45)
    relationship = models.CharField(max_length=45, null=True, blank=True)
    contactno = models.CharField(max_length=45, null=True, blank=True)
    def __unicode__(self):
        return self.fullname

class Curriculumvitae(models.Model):
    Firstname = models.CharField(max_length=45, null=True, blank=True)
    Surname = models.CharField(max_length=45, null=True, blank=True)
    Gender = models.CharField(max_length=45, null=True, blank=True)
    Email = models.CharField(max_length=45, null=True, blank=True)
    TelephoneNumber = models.CharField(max_length=45, null=True, blank=True)
    Location = models.CharField(max_length=45, null=True, blank=True)
    StreetName = models.CharField(max_length=45, null=True, blank=True)
    School = models.CharField(max_length=45, null=True, blank=True)
    HighestGrade = models.CharField(max_length=45, null=True, blank=True)
    HighestGradeYear = models.IntegerField(default=0, null=True, blank=True)
    DateOfBirth = models.CharField(max_length=45, null=True, blank=True)
    HouseNumber = models.CharField(max_length=45, null=True, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    workExperiences = models.ManyToManyField(Workexperience, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        if self.Firstname:
            return self.Firstname
        else:
            return str(self.id)

def create_cv(sender, instance, created, **kwargs):
    if created:
        cv = Curriculumvitae.objects.create(Firstname=instance.first_name, 
                Surname=instance.last_name, Email=instance.email,
                user=instance)
    else:
        cv = instance.get_profile()
        cv.Firstname = instance.first_name
        cv.Surname = instance.last_name
        cv.Email = instance.email
        cv.save()

post_save.connect(create_cv, sender=User)
