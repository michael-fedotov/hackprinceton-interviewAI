from django import forms


class CreateNewList(forms.Form):
    job_title = forms.CharField(label="Enter The Job Title", max_length=255)
    job_description = forms.CharField(label="Enter The Job Description", max_length=255)
