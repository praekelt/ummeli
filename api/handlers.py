from piston.handler import BaseHandler
from ummeli.webservice.models import (Certificate, Language, Workexperience,
    Reference, Curriculumvitae)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class CertificateHandler(BaseHandler):
    model = Certificate
    exclude = ('_state','id')

class LanguageHandler(BaseHandler):
    model = Language
    exclude = ('_state','id')

class WorkexperienceHandler(BaseHandler):
    model = Workexperience
    exclude = ('_state','id')

class ReferenceHandler(BaseHandler):
    model = Reference
    exclude = ('_state','id')

class CurriculumvitaeHandler(BaseHandler):
    model = Curriculumvitae
    fields = (('Firstname', 'Surname', 'Gender', 'Email',
        'TelephoneNumber','Location', 'StreetName', 
        'School', 'HighestGrade', 'HighestGradeYear', 
        'DateOfBirth', 'HouseNumber', ('certificates',()) ,
        ('languages',()) , ('workExperiences',()) , ('references',()) ))
    exclude = ('_state','id')

class UserHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    
    def read(self, request):
        username = request.GET.get('username')
        user = get_object_or_404(User, username = username)
        return user.get_profile()
