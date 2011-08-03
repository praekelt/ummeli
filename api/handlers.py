from piston.handler import BaseHandler
from ummeli.webservice.models import *

class UserHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = User
	fields = ('username',('cv',('Firstname', 'Surname', 'Gender', 'Email', 'TelephoneNumber', 'Location', 'StreetName', 'School', 'HighestGrade', 'HighestGradeYear', 'DateOfBirth', 'HouseNumber', ('certificates',()) , ('languages',()) , ('workExperiences',()) , ('references',()) )))
	
	def read(self, request, username=None):
		if username:
		    return User.objects.select_related().get(username = username)
		else:
		    return 'no user requested'
