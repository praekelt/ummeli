from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae)
from django.forms import (ModelForm, CheckboxInput,  Form, EmailField,  
                                            RegexField,  CharField)
from django.forms.forms import BoundField
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
class PMLModelForm(ModelForm):
    def as_pml(self):
        output = []
        for name,  field in self.fields.items():
            bf = BoundField(self, field, name)
            output.append('<TEXT position="ABOVE">%(label_name)s</TEXT><FIELD name="%(field_name)s" type="text"/><br/>'
                      % {
                      'label_name' : conditional_escape(force_unicode(bf.label)),
                      'field_name' : bf.html_name})
        return mark_safe(u'\n'.join(output))

class PersonalDetailsForm(PMLModelForm):
    firstName = CharField(label = 'Firstname')
    dateOfBirth = CharField(label = 'Date of birth',  required=False)
    class Meta:
        model = CurriculumVitae
        fields = ('firstName', 'surname', 'dateOfBirth', 'gender')

class ContactDetailsForm(PMLModelForm):
    telephoneNumber= CharField(label = 'Phone number',  required=False)
    email = CharField(label = 'Email address',  required=False)
    houseNumber = CharField(label = 'House number',  required=False)
    streetName = CharField(label = 'Street name',  required=False)
    location = CharField(label = 'Location name',  required=False)
    class Meta:
        model = CurriculumVitae
        fields = ('telephoneNumber', 'email', 'houseNumber', 'streetName',
                'location')

class EducationDetailsForm(PMLModelForm):
    highestGrade = CharField(label = 'Highest grade passed',  required=False)
    highestGradeYear = CharField(label = 'Year passed',  required=False)
    school = CharField(label = 'Name of school', required=False)
    class Meta:
        model = CurriculumVitae
        fields = ('highestGrade', 'highestGradeYear', 'school')

class CertificateForm(PMLModelForm):
    name = CharField(label = 'Name of Certificate')
    institution = CharField(label = 'Name of institution', required=False)
    year = CharField(label = 'Year completed', required=False)
    class Meta:
        model = Certificate
        
class WorkExperienceForm(PMLModelForm):
    class Meta:
        model = WorkExperience

class LanguageForm(PMLModelForm):
    language = CharField(label = 'Name of language')
    readWrite = CharField(label = 'Can you Read and Write in this language')
    class Meta:
        model = Language
        widgets = {'readWrite': CheckboxInput(),}

class ReferenceForm(PMLModelForm):
    class Meta:
        model = Reference

class SendEmailForm(Form):
    email = EmailField()

class SendFaxForm(Form):
    fax = RegexField('[0-9+]',  error_message='Please enter a valid fax number.')
