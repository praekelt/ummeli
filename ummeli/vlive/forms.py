from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae)
from django.forms import (ModelForm, CheckboxInput,  Form, EmailField,  
                                            RegexField)
from django.forms.forms import BoundField
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
class PMLModelForm(ModelForm):
    def as_pml(self):
        output = []
        for name,  field in self.fields.items():
            bf = BoundField(self, field, name)
            output.append('<TEXT position="ABOVE">%(label_name)s</TEXT><FIELD name="%(field_name)s" type="text"/>'
                      % {
                      'label_name' : conditional_escape(force_unicode(bf.label)),
                      'field_name' : bf.html_name})
        return mark_safe(u'\n'.join(output))

class PersonalDetailsForm(PMLModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ('firstName', 'surname', 'dateOfBirth', 'gender')

class ContactDetailsForm(PMLModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ('telephoneNumber', 'email', 'houseNumber', 'streetName',
                'location')

class EducationDetailsForm(PMLModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ('highestGrade', 'highestGradeYear', 'school')

class CertificateForm(PMLModelForm):
    class Meta:
        model = Certificate
        
class WorkExperienceForm(PMLModelForm):
    class Meta:
        model = WorkExperience

class LanguageForm(PMLModelForm):
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
