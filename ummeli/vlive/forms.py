from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae)
from django.forms import ModelForm, CheckboxInput
        
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

class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        
class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience

class LanguageForm(ModelForm):
    class Meta:
        model = Language
        widgets = {'readWrite': CheckboxInput(),}

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference

