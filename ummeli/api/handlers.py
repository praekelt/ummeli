from piston.handler import BaseHandler
from piston.utils import rc
from ummeli.api.models import (Certificate, Language, Workexperience,
    Reference, Curriculumvitae, CurriculumvitaeForm)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class CertificateHandler(BaseHandler):
    model = Certificate
    exclude = ('_state')

class LanguageHandler(BaseHandler):
    model = Language
    exclude = ('_state')

class WorkexperienceHandler(BaseHandler):
    model = Workexperience
    exclude = ('_state')

class ReferenceHandler(BaseHandler):
    model = Reference
    exclude = ('_state')

class CurriculumvitaeHandler(BaseHandler):
    model = Curriculumvitae
    fields = (('id','Firstname', 'Surname', 'Gender', 'Email',
        'TelephoneNumber','Location', 'StreetName', 
        'School', 'HighestGrade', 'HighestGradeYear', 
        'DateOfBirth', 'HouseNumber', ('certificates',()) ,
        ('languages',()) , ('workExperiences',()) , ('references',()) ))
    exclude = ('_state')

class UserHandler(BaseHandler):
    allowed_methods = ('GET','POST','PUT',)
    
    def read(self, request):
        username = request.GET.get('username')
        user = get_object_or_404(User, username = username)
        return user.get_profile()
    
    def create(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username = username):
            response = rc.DUPLICATE_ENTRY
            response.write('User already exists')
            return response
        else:
            user = User.objects.create(username=username, password=password)
            return user.get_profile()
    
    def update(self, request):
        cv_id = request.POST.get('id')
        cv = get_object_or_404(Curriculumvitae, pk=cv_id)
        cvform = CurriculumvitaeForm(request.POST, instance=cv)
        return cvform.save()