from piston.handler import BaseHandler
from piston.utils import rc
from ummeli.webservice.models import *
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
    model = UserProfile
    fields = ('username',('cv',()))
    
    def read(self, request):
        username = request.GET.get('username')       
        user = get_object_or_404(User,username = username)
        UserProfile.objects.get_or_create(user = user, defaults = {'cv': Curriculumvitae.objects.create(Firstname='',Surname='')})
        return user.get_profile()
        '''if username:
            user = User.objects.filter(username = username)
            if user:
                return user[0]
            else:
                response = rc.NOT_FOUND    
                response.write(' - user not found')
                return response                
        else:
            response = rc.BAD_REQUEST    
            response.write(' - no user specified')
            return response
        '''
