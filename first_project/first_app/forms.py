from django import forms


class CreateNewList(forms.Form):
    job_title = forms.CharField(label="job_title", max_length=255)
    job_description = forms.CharField(label="job_description", max_length=255)
