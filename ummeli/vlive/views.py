from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

@login_required
def index(request):    
    cv = request.user.get_profile()
    return render_to_response('vlive/cv.html', {'cv': cv})