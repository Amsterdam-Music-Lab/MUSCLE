import csv
from http import HTTPStatus

from django import forms
from django.core.exceptions import ValidationError
from .models import Playlist

from section.validators import audio_file_validator, file_exists_validator


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AddSections(forms.Form):
    artist = forms.CharField(max_length=128, required=False)
    name = forms.CharField(max_length=128, required=False)
    tag = forms.CharField(max_length=128, required=False)
    group = forms.CharField(max_length=128, required=False)
    files = forms.FileField(widget=MultipleFileInput(
        attrs={'accept': '.wav,.mp3,.aiff,.flac,.ogg'}),
        validators=[audio_file_validator()])


class PlaylistAdminForm(forms.ModelForm):
    csv_file = forms.FileField(required=False,
                               help_text='Upload a CSV file \
                                (overrides the text input above)',
                               label='CSV file',
                               widget=forms.FileInput(attrs={'accept': '.csv'})
                               )

    class Meta:
        model = Playlist
        fields = '__all__'
        help_texts = {
            'url_prefix': 
                'URL for hosting the audio files on an external server.<br> \
                Make sure the path of the audio file is valid.<br> \
                Leave this empty if you host the audio files locally.'}

        widgets = {'url_prefix': forms.TextInput(attrs={'size': '37',
                   'placeholder': 'https://example.com/'})
                   }

    def clean_csv(self):
        """Validate the csv file"""
        super().clean()

        url_prefix = self.cleaned_data['url_prefix']

        csv_data = self.cleaned_data['csv']

        # We do not check external files
        if url_prefix:
            return csv_data

        try:
            reader = csv.DictReader(csv_data.splitlines(), fieldnames=(
                'artist', 'name', 'start_time', 'duration', 'filename', 'tag', 'group'))
        except csv.Error:
            return {
                'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': "Error: could not initialize csv.DictReader"
            }

        for row in reader:
            # Check if the file exists
            try:
                file_exists_validator(row['filename'])
            except ValidationError as e:
                self.add_error('csv', e)

        return csv_data

    def save(self, commit=True):
        playlist = super().save(commit=False)

        # Handle uploaded CSV file
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file and playlist.process_csv:
            # Read and process the CSV file
            playlist.csv = csv_file.read().decode('utf-8')

        if commit:
            playlist.save()

        return playlist
