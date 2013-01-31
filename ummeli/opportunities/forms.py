from django import forms
from ummeli.opportunities.models import TomTomMicroTaskResponse
from ummeli.vlive.utils import get_lat_lon


class TomTomMicroTaskResponseForm(forms.ModelForm):
    class Meta:
        model = TomTomMicroTaskResponse
        exclude = ('task', 'user', 'state')

    def clean_file(self):
        file = self.cleaned_data['file']
        lat, lon = get_lat_lon(file)

        if lat and lon:
            return file

        raise forms.ValidationError("Your image does not contain GPS information. Please read the instructions and try again.")
