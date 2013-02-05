from django import forms


class UploadTaskForm(forms.Form):
    file = forms.FileField()


class TaskResponseForm(forms.Form):
    accept = forms.BooleanField(required=False)
    username = forms.CharField()
    response_id = forms.IntegerField()
