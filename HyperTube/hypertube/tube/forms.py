
from django import forms


class VideoUploadForm(forms.Form):
    video = forms.FileField(label='Select a video')
    title = forms.CharField(label='Title', max_length=255)
    tags = forms.CharField(label='Point tags', max_length=255)