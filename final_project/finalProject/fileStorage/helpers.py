from django import forms

class FileUploadForm(forms.Form):
    filename = forms.CharField(max_length=100, label='Enter file name')
    fileDescription = forms.CharField(widget=forms.Textarea, label='Enter file description')
    file = forms.FileField(label='Select file')
