from django import forms
from ummeli.opportunities.models import TomTomMicroTaskResponse
from ummeli.vlive.utils import get_lat_lon


class TomTomMicroTaskResponseForm(forms.ModelForm):
    tel_1 = forms.CharField(required=False)
    tel_2 = forms.CharField(required=False)
    fax = forms.CharField(required=False)
    email = forms.CharField(required=False)
    website = forms.CharField(required=False)
    address = forms.CharField(required=False)
    comment = forms.CharField(required=False)

    class Meta:
        model = TomTomMicroTaskResponse
        exclude = ('task', 'user', 'state', 'task_checkout')

    def clean_file(self):
        file = self.cleaned_data['file']
        lat, lon = get_lat_lon(file)

        if lat and lon:
            return file

        raise forms.ValidationError("Your image does not contain GPS information. Please read the instructions and try again.")
