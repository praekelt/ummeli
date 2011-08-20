from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae)
from django.forms import ModelForm
        
class PersonalDetailsForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ('firstName', 'surname', 'dateOfBirth', 'gender')

class ContactDetailsForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ('telephoneNumber', 'email', 'houseNumber', 'streetName',
                'location')

class EducationDetailsForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ('highestGrade', 'highestGradeYear', 'school')

