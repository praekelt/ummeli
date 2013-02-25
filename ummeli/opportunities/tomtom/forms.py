from django import forms
from ummeli.opportunities.models import TomTomMicroTaskResponse
from ummeli.vlive.utils import get_lat_lon


class MicroTaskResponseForm(forms.ModelForm):
    tel_1 = forms.RegexField('[0-9+]', required=False,
                error_message='Please enter a valid telephone number.')
    tel_2 = forms.RegexField('[0-9+]', required=False,
                error_message='Please enter a valid telephone number.')
    fax = forms.RegexField('[0-9+]', required=False,
                error_message='Please enter a valid fax number.')
    email = forms.EmailField(required=False, error_messages={
                'invalid': 'Please enter a valid email address.'})
    website = forms.URLField(required=False, error_messages={
                'invalid': 'Please enter a valid website address.'})
    address = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    poi_has_changed = forms.BooleanField(required=False)
    file = forms.FileField(required=True, error_messages={
                'required': 'Please choose a valid photo to upload.',
                'invalid': 'Please choose a valid photo to upload.',
                })

    class Meta:
        model = TomTomMicroTaskResponse
        exclude = ('task', 'user', 'state', 'task_checkout')

    def clean_file(self):
        file = self.cleaned_data['file']
        lat, lon = get_lat_lon(file)

        if not lat == None and not lon == None:
            return file

        error = ("Your image does not contain GPS information. "
                "Please read the instructions and try again.")
        raise forms.ValidationError(error)


class SelectLocationForm(forms.Form):
    error = forms.BooleanField(required=False)


class ChangeDeviceForm(forms.Form):
    device = forms.CharField(required=True,
                error_messages={'required': 'Please choose a device'})
