from django import forms
from .models import Playlist

from .validators import audio_file_validator


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AddSections(forms.Form):
    artist = forms.CharField(max_length=128, required=False)
    name = forms.CharField(max_length=128, required=False)
    tag = forms.CharField(max_length=128, required=False)
    group = forms.CharField(max_length=128, required=False)
    files = forms.FileField(widget=MultipleFileInput(attrs={'accept':'.wav,.mp3,.aiff,.flac,.ogg'}),
                            validators=[audio_file_validator()])


class PlaylistAdminForm(forms.ModelForm):
    csv_file = forms.FileField(required=False, help_text='Upload a CSV file (overrides the text input above)', label='CSV file', widget=forms.FileInput(attrs={'accept':'.csv'}))

    class Meta:
        model = Playlist
        fields = '__all__'

    def save(self, commit=True):
        playlist = super().save(commit=False)

        # Handle uploaded CSV file
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            # Read and process the CSV file
            playlist.csv = csv_file.read().decode('utf-8')

        if commit:
            playlist.save()

        return playlist
