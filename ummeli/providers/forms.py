from django import forms


class UploadTaskForm(forms.Form):
    file = forms.FileField()


class TaskResponseForm(forms.Form):
    accept = forms.BooleanField(required=False)
    username = forms.CharField()
    reject_comment = forms.CharField(required=False)
    reject_reason = forms.IntegerField()
    response_id = forms.IntegerField()
