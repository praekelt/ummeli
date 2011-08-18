from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

@login_required
def personal_details(request):    
    return render_to_response('vlive/cv.html')
