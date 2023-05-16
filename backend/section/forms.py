from django import forms

class AddSections(forms.Form):

    artist = forms.CharField(max_length=128, required=False)
    name = forms.CharField(max_length=128, required=False)
    tag = forms.CharField(max_length=128, required=False)
    group = forms.CharField(max_length=128, required=False)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
