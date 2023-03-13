from django import forms
from section.models import Playlist, Section

class AddSections(forms.Form):

    artist = forms.CharField(max_length=128)
    name = forms.CharField(max_length=128)    
    tag = forms.CharField(max_length=128)
    group = forms.CharField(max_length=128)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
