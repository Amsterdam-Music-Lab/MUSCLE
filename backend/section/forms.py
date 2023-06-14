from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class AddSections(forms.Form):

    artist = forms.CharField(max_length=128, required=False)
    name = forms.CharField(max_length=128, required=False)
    tag = forms.CharField(max_length=128, required=False)
    group = forms.CharField(max_length=128, required=False)
    files = forms.FileField(widget=MultipleFileInput)
