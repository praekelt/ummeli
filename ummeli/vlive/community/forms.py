from django import forms
from ummeli.opportunities.models import Job, Province, CATEGORY_CHOICES
from ummeli.vlive.forms import PMLModelForm, PMLForm


class StatusUpdateForm(PMLForm):
    title = forms.CharField(label='Status', required=True, max_length=160)


class JobEditForm(PMLModelForm):
    province = forms.ModelChoiceField(empty_label=None, queryset=Province.objects.all(), label='Province', required=True)
    category = forms.IntegerField(widget=forms.Select(choices=CATEGORY_CHOICES),
                                  required=True,
                                  min_value=1,
                                  error_messages={'min_value': 'Please choose a category.'})
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(label='Description',
                                  required=True,
                                  help_text='Please provide as much information about the job as possible including contact details.')

    class Meta:
        model = Job
        fields = ('province', 'category', 'title', 'description')
