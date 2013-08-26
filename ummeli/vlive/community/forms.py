from django import forms
from ummeli.opportunities.models import *
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


class OpportunityEditForm(PMLForm):
    BURSARY = 1
    TRAINING = 2
    VOLUNTEERING = 3
    INTERNSHIP = 4
    OPPORTUNITY_CHOICES = [(0, 'Please select'),
                           (BURSARY, 'Bursary'),
                           (TRAINING, 'Training'),
                           (VOLUNTEERING, 'Volunteering'),
                           (INTERNSHIP, 'Internship')]

    opportunity_type = forms.IntegerField(widget=forms.Select(choices=OPPORTUNITY_CHOICES),
                                          required=True,
                                          min_value=1,
                                          error_messages={'min_value': 'Please choose an opportunity type.'})
    province = forms.ChoiceField(choices=[(p.pk, p.get_province_display()) for p in Province.objects.all()], label='Province', required=True)
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(label='Description',
                                  required=True,
                                  help_text='Please provide as much information about the opportunity as possible including contact details.')

    def get_model(self):
        if self.is_valid():
            opportunity_type = self.cleaned_data['opportunity_type']

            if opportunity_type == self.BURSARY:
                return Bursary

            if opportunity_type == self.TRAINING:
                return Training

            if opportunity_type == self.VOLUNTEERING:
                return Volunteer

            if opportunity_type == self.INTERNSHIP:
                return Internship
        return None

