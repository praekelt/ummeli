from django import forms


class StatusUpdateForm(forms.Form):
    title = forms.CharField(label='Status', required=True)
