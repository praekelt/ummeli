from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae)
from django.forms import (ModelForm, CheckboxInput,  Form, EmailField,  
                                            RegexField,  CharField,  BooleanField,  IntegerField)
from django.forms.forms import BoundField
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

def format_as_pml(self):
    output = []
    for name,  field in self.fields.items():
        bf = BoundField(self, field, name)
        
        text_field_type = 'Text'
        
        if(isinstance(field, IntegerField)):
            text_field_type = 'num'
        
        field_str = ('<TEXT position="ABOVE">%(label_name)s</TEXT><FIELD name="%(field_name)s" type="%(text_field_type)s" default="%(field_value)s"/><br/>'
                % {
                  'label_name' : conditional_escape(force_unicode(bf.label)),
                  'field_name' : bf.html_name, 
                  'field_value' : bf.value()  if bf.value() != None  else '', 
                  'text_field_type' : text_field_type
                  })
        if(isinstance(field, BooleanField)):
            default = bf.value()  if bf.value() != None  else ''
            
            field_str = ('''<CHOICE-GROUP type="radio" name="%(field_name)s">
            <TEXT>%(label_name)s</TEXT>
            <CHOICE value="True" checked="%(default_true)s">Yes</CHOICE>
            <CHOICE value="False" checked="%(default_false)s">No</CHOICE>
            </CHOICE-GROUP>''' %
            {
                'default_true':  'true' if default else 'false', 
                'default_false':  'true' if not default else 'false', 
                'label_name' : conditional_escape(force_unicode(bf.label)),
                'field_name' : bf.html_name, 
                'field_value' : bf.value()  if bf.value() != None  else '' 
            })
        
        if(bf.errors):
            bf_errors = u'\n'.join([u'<TEXT position="ABOVE">%s</TEXT>' 
                                    % conditional_escape(force_unicode(error)) for error in bf.errors])
            output.append(mark_safe(bf_errors))
        
        output.append(field_str )
    return mark_safe(u'\n'.join(output))
        
class PMLModelForm(ModelForm):
    def as_pml(self):
        return format_as_pml(self)

class PMLForm(Form):
    def as_pml(self):
        return format_as_pml(self)

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
    highestGradeYear = IntegerField(label = 'Year passed',  required=False)
    school = CharField(label = 'Name of school', required=False)
    class Meta:
        model = CurriculumVitae
        fields = ('highestGrade', 'highestGradeYear', 'school')

class CertificateForm(PMLModelForm):
    name = CharField(label = 'Name of Certificate')
    institution = CharField(label = 'Name of institution', required=False)
    year = IntegerField(label = 'Year completed', required=False)
    class Meta:
        model = Certificate
        
class WorkExperienceForm(PMLModelForm):
    class Meta:
        model = WorkExperience

class LanguageForm(PMLModelForm):
    language = CharField(label = 'Name of language')
    readWrite = BooleanField(label = 'Can you Read and Write in this language')
    class Meta:
        model = Language
        widgets = {'readWrite': CheckboxInput(),}

class ReferenceForm(PMLModelForm):
    class Meta:
        model = Reference

class SendEmailForm(PMLForm):
    email = EmailField()

class SendFaxForm(PMLForm):
    fax = RegexField('[0-9+]',  error_message='Please enter a valid fax number.')
