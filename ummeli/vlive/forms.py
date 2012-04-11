from ummeli.base.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae,  UserSubmittedJobArticle, Skill, SKILL_LEVEL_CHOICES)
from django.forms import (ModelForm, CheckboxInput,  Form, EmailField,
                          RegexField,  CharField,  BooleanField,  IntegerField,
                          Textarea,  ValidationError, RadioSelect)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import BoundField
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

def format_errors_as_pml(self):
    bf_errors = []
    for name,  field in self.fields.items():
        bf = BoundField(self, field, name)

        if(bf.errors):
            for error in bf.errors:
                bf_error = u'\n'.join([u'<TEXT position="ABOVE"><color value="red">%(label_name)s - %(error_message)s</color></TEXT><br/>'
                            % {
                            'label_name': conditional_escape(force_unicode(bf.label)),
                            'error_message': conditional_escape(force_unicode(error))
                            }])
                bf_errors.append(mark_safe(bf_error))
    return mark_safe(u'\n'.join(bf_errors))

def format_as_pml(self):
    output = []
    for name,  field in self.fields.items():
        bf = BoundField(self, field, name)

        text_field_type = 'Text'

        if(isinstance(field, IntegerField)):
            text_field_type = 'num'

        field_str = ('<TEXT position="ABOVE">%(label_name)s</TEXT><FIELD name="%(field_name)s" type="%(text_field_type)s" default="%(field_value)s"/><br/>'
                % {
                  'label_name': conditional_escape(force_unicode(bf.label)),
                  'field_name': bf.html_name,
                  'field_value': bf.value()  if bf.value() != None  else '',
                  'text_field_type': text_field_type
                  })
        if(isinstance(field, BooleanField)):
            default = bf.value()  if bf.value() != None  else ''

            field_str = ('''<CHOICE-GROUP type="radio" name="%(field_name)s">
            <TEXT>%(label_name)s</TEXT>
            <CHOICE value="True" %(default_true)s>Yes</CHOICE>
            <CHOICE value="False" %(default_false)s>No</CHOICE>
            </CHOICE-GROUP>''' %
            {
                'default_true':  'checked="true"' if default else '',
                'default_false':  'checked="true"' if not default else '',
                'label_name': conditional_escape(force_unicode(bf.label)),
                'field_name': bf.html_name,
                'field_value': bf.value()  if bf.value() != None  else ''
            })

        output.append(field_str)
    return mark_safe(u'\n'.join(output))

class PMLModelForm(ModelForm):
    def as_pml(self):
        return format_as_pml(self)

    def errors_as_pml(self):
        return format_errors_as_pml(self)

class PMLForm(Form):
    def as_pml(self):
        return format_as_pml(self)

    def errors_as_pml(self):
        return format_errors_as_pml(self)

class PersonalDetailsForm(PMLModelForm):
    first_name = CharField(label = 'First name', required = True)
    date_of_birth = CharField(label = 'Date of birth',  required = False)

    class Meta:
        model = CurriculumVitae
        fields = ('first_name', 'surname', 'date_of_birth', 'gender')

class ContactDetailsForm(PMLModelForm):
    telephone_number = CharField(label = 'Phone number',  required = True)
    email = CharField(label = 'Email address',  required = False)
    address = CharField(label = 'Address',  required = False)
    city = CharField(label = 'City',  required = True)

    class Meta:
        model = CurriculumVitae
        fields = ('telephone_number', 'email', 'address', 'city')

class PersonalStatementForm(PMLModelForm):
    about_me = CharField(label = 'Personal Statement',  required = True)

    class Meta:
        model = CurriculumVitae
        fields = ('about_me',)

class EducationDetailsForm(PMLModelForm):
    highest_grade = IntegerField(label = 'Highest grade passed',  required = False)
    highest_grade_year = IntegerField(label = 'Year passed',  required = False)
    school = CharField(label = 'Name of school', required = False)

    class Meta:
        model = CurriculumVitae
        fields = ('highest_grade', 'highest_grade_year', 'school')

class CertificateForm(PMLModelForm):
    name = CharField(label = 'Name of certificate')
    institution = CharField(label = 'Name of institution', required = False)
    year = IntegerField(label = 'Year completed', required = False)
    duration = IntegerField(label = 'Duration', required = False)

    class Meta:
        model = Certificate

class WorkExperienceForm(PMLModelForm):
    title = CharField(label = 'Job title')
    company = CharField(label = 'Name of company')
    start_year = IntegerField(label = 'Year started')
    end_year = IntegerField(label = 'Year ended')

    class Meta:
        model = WorkExperience

class LanguageForm(PMLModelForm):
    language = CharField(label = 'Name of language')
    read_write = BooleanField(label = 'Can you Read and Write in this language',
                                            required = False)

    class Meta:
        model = Language
        widgets = {'read_write': CheckboxInput(),}

class ReferenceForm(PMLModelForm):
    fullname = CharField(label = 'Fullname')
    relationship = CharField(label = 'Relationship (title)')
    contact_no = CharField(label = 'Contact number')

    class Meta:
        model = Reference

class SkillForm(PMLModelForm):
    class Meta:
        model = Skill
        
    skill = CharField(label = 'Skill')
    level = IntegerField(widget=RadioSelect(choices=SKILL_LEVEL_CHOICES))
        
class SkillWizardForm(PMLForm):
    skill = CharField(label = 'Skill')
        
class SkillWizardFormPick(PMLForm):
    selected_skill = CharField(label = 'Skill')


class EmailCVForm(PMLForm):
    send_via = CharField(required = True)
    send_to = EmailField(required = True)
    send_message = CharField(required = False)

class FaxCVForm(PMLForm):
    send_via = CharField(required = True)
    send_to = RegexField('[0-9+]', required = True,
                                    error_message = 'Please enter a valid fax number.')
    send_message = CharField(required = False)

class UserSubmittedJobArticleForm(PMLModelForm):
    province = IntegerField(required = True)
    category = CharField(required = True)
    title = CharField(required = True)
    text = CharField(required = True,  widget = Textarea,  label = 'Description')

    class Meta:
        model = UserSubmittedJobArticle
        fields = ('title',  'text')
        
class UserSubmittedJobArticleEditForm(PMLModelForm):
    province = CharField(required = True)
    job_category = CharField(required = True)
    title = CharField(required = True)
    text = CharField(required = True,  widget = Textarea,  label = 'Description')

    class Meta:
        model = UserSubmittedJobArticle
        fields = ('title',  'text', 'province', 'job_category')

class ForgotPasswordForm(Form):
    username = RegexField('[0-9+]', required = True,
                          error_message = 'Please enter a valid cellphone number.', 
                          label="Enter the cellphone number to reset the pin for.")
                          
    def clean_username(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        username = self.cleaned_data["username"]
        self.users_cache = User.objects.filter(username__iexact=username)
        if not self.users_cache.exists():
            raise ValidationError("That cellphone number doesn't have an associated user account. Are you sure you've registered?")
        return username


class MobiUserCreationForm(UserCreationForm):
    username = RegexField(
        label='Phone number', 
        regex=r'^[0-9]+$',
        help_text = 'Required. Valid phone number in the format: 0821234567',
        error_message = 'Please enter a valid phone number without spaces. e.g 0821234567')


class ConcactSupportForm(PMLForm):
    username = CharField(required = True)
    message = CharField(required = True,  widget = Textarea)
