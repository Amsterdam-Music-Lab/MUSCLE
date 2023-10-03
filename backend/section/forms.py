from django import forms

from .validators import audio_file_validator

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class AddSections(forms.Form):
    artist = forms.CharField(max_length=128, required=False)
    name = forms.CharField(max_length=128, required=False)
    tag = forms.CharField(max_length=128, required=False)
    group = forms.CharField(max_length=128, required=False)
    files = forms.FileField(widget=MultipleFileInput, validators=[audio_file_validator()])
