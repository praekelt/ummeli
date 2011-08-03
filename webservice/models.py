from django.db import models

class User(models.Model):
	username = models.CharField(max_length=45, primary_key=True)
	password = models.CharField(max_length=8000)
	sendPhoneNumber = models.CharField(max_length=45, null=True, blank=True)
	sendFaxNumber = models.CharField(max_length=45, null=True, blank=True)
	sendEmail = models.CharField(max_length=45, null=True, blank=True)
	RequiredJobs = models.CharField(max_length=8000, null=True, blank=True)
	RequiredTraining = models.CharField(max_length=8000, null=True, blank=True)
	def __unicode__(self):
		return self.username
		
class Curriculumvitae (models.Model):
	user = models.ForeignKey(User, unique=True)
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
	def __unicode__(self):
		return self.Firstname + " "+ self.Surname
		
class Certificate (models.Model):
	cv = models.ForeignKey(Curriculumvitae)
	name = models.CharField(max_length=45)
	institution = models.CharField(max_length=200, null=True, blank=True)
	year = models.IntegerField(default=0, null=True, blank=True)
	def __unicode__(self):
		return self.name + " @ "+ self.institution
		
class Language (models.Model):
	cv = models.ForeignKey(Curriculumvitae)
	language = models.CharField(max_length=45)
	readwrite = models.IntegerField(default=0)
	def __unicode__(self):
		return self.language
		
class Workexperience (models.Model):
	cv = models.ForeignKey(Curriculumvitae)
	title = models.CharField(max_length=45)
	company = models.CharField(max_length=45, null=True, blank=True)
	startyear = models.IntegerField(default=0, null=True, blank=True)
	endyear = models.IntegerField(default=0, null=True, blank=True)
	def __unicode__(self):
		return self.title + " @ "+ self.company
		
class Reference (models.Model):
	cv = models.ForeignKey(Curriculumvitae)
	fullname = models.CharField(max_length=45)
	relationship = models.CharField(max_length=45, null=True, blank=True)
	contactno = models.CharField(max_length=45, null=True, blank=True)
	def __unicode__(self):
		return self.fullname