from django import forms


class UploadTaskForm(forms.Form):
    file = forms.FileField()
