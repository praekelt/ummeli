from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae)
from django.forms import ModelForm
        
class PersonalDetailsForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        exclude = ('user', 'references', 'workExperiences', 'languages',
                'certificates')

