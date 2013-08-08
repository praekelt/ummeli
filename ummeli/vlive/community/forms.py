from django import forms
from ummeli.opportunities.models import Job, Province, CATEGORY_CHOICES

class StatusUpdateForm(forms.Form):
    title = forms.CharField(label='Status', required=True, max_length=160)


class JobEditForm(forms.Form):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), label='Province', required=True)
    category = forms.IntegerField(widget=forms.Select(choices=CATEGORY_CHOICES), required=True)
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(label='Description', required=True, help_text='Please provide as much information about the job as possible including contact details.')

    class Meta:
        model = Job
