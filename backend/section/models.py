"""
Models for managing audio files used in experiments

Our examples will assume that a playlist with the following csv data has been added to an empty database:
```
(
    "Lion King,Hakuna Matata,0.0,10.0,/my/experiment/lionking1.mp3,Disney,happy"
    "Lion King,Hakuna Matata,30.0,10.0,/my/experiment/lionking2.mp3,Disney,happy"
    "Frozen,Let It Go,0.0,10.0,/my/experiment/frozen1.mp3,Disney,sad"
    "Frozen,Let It Go,30.0,10.0,/my/experiment/frozen2.mp3,Disney,sad"
    "West Side Story,America,0.0,10.0,/my/experiment/westsidestory1.mp3,Musical,happy"
    "West Side Story,America,30.0,10.0,/my/experiment/westsidestory2.mp3,Musical,happy"
    "Porgy & Bess,Summertime,0.0,10.0,/my/experiment/porgyandbess1.mp3,Musical,sad"
    "Porgy & Bess,Summertime,30.0,10.0,/my/experiment/porgyandbess2.mp3,Musical,sad"
)
```
"""

import datetime
import random
import csv
from os.path import join
import audioread

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError

from .utils import CsvStringBuilder, get_or_create_song
from section.validators import (
    audio_file_validator, file_exists_validator, url_prefix_validator
)


class Playlist(models.Model):
    """A model defining a list of sections to be played in a Block

    Attributes:
        name (str): playlist name
        url_prefix (str): prefix for sections served from an external site
        process_csv (bool): whether a csv file should be processed to create or edit this playlist
        csv (str): a csv file which can be processed to create or edit this playlist
    """

    name = models.CharField(db_index=True, max_length=64)
    url_prefix = models.CharField(max_length=128,
                                  blank=True,
                                  default='',
                                  validators=[url_prefix_validator])

    process_warning = 'Warning: Processing a live playlist may affect the result data'
    process_csv = models.BooleanField(default=False, help_text=process_warning)

    default_csv_row = 'CSV Format: artist_name [string],\
        song_name [string], start_position [float], duration [float],\
        "path/filename.mp3" [string], tag [string], group [string]'
    csv = models.TextField(blank=True, help_text=default_csv_row)

    CSV_OK = 0
    CSV_ERROR = 10

    def clean_csv(self):
        errors = []
        sections = Section.objects.filter(playlist=self)

        for section in sections:
            filename = str(section.filename)

            try:
                file_exists_validator(filename)
            except ValidationError as e:
                errors.append(e)

        if errors:
            raise ValidationError(errors)

        return self.csv

    def save(self, *args, **kwargs):
        if self.process_csv is False and self.id:
            self.csv = self._update_admin_csv()
        if self.url_prefix and self.url_prefix[-1] != '/':
            self.url_prefix += '/'
        self.process_csv = False
        super(Playlist, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def _section_count(self):
        """Number of sections, as displayed in the admin interface"""
        return self.section_set.count()

    _section_count.short_description = "Sections"

    def _block_count(self):
        """Number of Blocks"""
        return self.block_set.count()

    _block_count.short_description = "Blocks"

    def _update_sections(self):
        """update sections associated with a Playlist object based on its `csv` field"""
        # CSV empty
        if len(self.csv) == 0:
            # Delete all existing sections
            self.section_set.all().delete()
            return {
                'status': self.CSV_OK,
                'message': "No sections added. Deleted all existing sections."
            }

        # Store existing sections
        existing_sections = [section for section in self.section_set.all()]

        # Add new sections from csv
        try:
            reader = csv.DictReader(self.csv.splitlines(), fieldnames=(
                'artist', 'name', 'start_time', 'duration', 'filename', 'tag', 'group'))
        except csv.Error:
            return {
                'status': self.CSV_ERROR,
                'message': "Error: could not initialize csv.DictReader"
            }

        def is_number(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        sections = []
        updated = 0
        lines = 0
        csv_messages = []
        global_errors = 0
        for row in reader:
            lines += 1
            iteration_error = False
            
            # Check for valid row length in csv. If it has less than 8 entries, csv.DictReader will assign None to values of missing keys            
            if None in row.values():
                csv_messages.append(f"Error: Invalid row length, line: {str(lines)}")
                # Skip adding or altering this row
                iteration_error = True
                global_errors += 1

            # check for valid numbers
            if not (is_number(row['start_time'])
                    and is_number(row['duration'])):
                csv_messages.append(f"Error: Expected number fields on line: {str(lines)}")
                # Skip adding or altering this row
                iteration_error = True
                global_errors += 1

            # Check if the duration in the csv exceeds the actual duration of the audio file
            file_path = join(settings.MEDIA_ROOT, str(row['filename']))

            try:
                # while running tests this would throw an error
                with audioread.audio_open(file_path) as f:
                    actual_duration = f.duration
                if float(row['duration']) > actual_duration:
                    # Add or edit this row, but show an error message containing the actual saved duration
                    row['duration'] = actual_duration
                    global_errors += 1
                    csv_messages.append(f"Error: The duration of {row['filename']} exceeds the actual duration of the audio file and has been set to {actual_duration} seconds.")
            except:
                pass
                
            # Make the changes if there are no global errors in this row
            if not iteration_error:
                # Retrieve or create Song object
                song = None
                if row['artist'] or row['name']:
                    song = get_or_create_song(row['artist'], row['name'])

                # create new section
                section = Section(playlist=self,
                                start_time=float(row['start_time']),
                                duration=float(row['duration']),
                                filename=row['filename'],
                                tag=row['tag'],
                                group=row['group'],
                                )
                section.song = song

                # if same section already exists, update it with new info
                for ex_section in existing_sections:
                    if ex_section.filename == section.filename:
                        if song:
                            ex_section.song = song
                            ex_section.save()
                        ex_section.start_time = section.start_time
                        ex_section.duration = section.duration
                        ex_section.tag = section.tag
                        ex_section.group = section.group
                        ex_section.save()
                        updated += 1

                        # Remove from existing sections list
                        existing_sections.remove(ex_section)
                        section = None
                        break

                # append section
                if section:
                    sections.append(section)

        # No global errors
        if global_errors == 0:

            # Add sections
            Section.objects.bulk_create(sections)

            # Remove obsolete sections
            delete_ids = [ex_section.id for ex_section in existing_sections]
            self.section_set.filter(pk__in=delete_ids).delete()

            # Reset process csv option and save playlist
            self.process_csv = False
            self.save()
            
            return {
                'status': self.CSV_OK,
                'message':
                  f"Sections processed from CSV. Added: {str(len(sections))} - Updated: {str(updated)} - Removed: {str(len(delete_ids))}"
            }

        return {
                    'status': self.CSV_ERROR,
                    'messages': csv_messages,
                }

    def _export_admin(self):
        """Export data for admin"""
        return {
            "exportedAt": timezone.now().isoformat(),
            "playlist": {
                "id": self.id,
                "name": self.name,
                "sections": [
                    section._export_admin() for section in self.section_set.all()
                ],
            },
        }

    def _export_sections(self):
        # export section objects
        return self.section_set.all()

    def _update_admin_csv(self):
        """Update csv data for admin"""
        csvfile = CsvStringBuilder()
        writer = csv.writer(csvfile)
        for section in self.section_set.all():
            if section.song:
                this_artist = section.artist_name()
                this_name = section.song_name()
            else:
                this_artist = ''
                this_name = ''
            writer.writerow([this_artist,
                            this_name,
                            section.start_time,
                            section.duration,
                            section.filename,
                            section.tag,
                            section.group])
        csv_string = csvfile.csv_string
        return ''.join(csv_string)

    def get_section(
        self, filter_by: dict = {}, exclude: dict = {}, song_ids: list = []
    ):
        """Get a random section from this playlist
        Optionally, limit to specific song_ids and filter conditions
        `filter_by` and `exclude` use [Django's querying syntax](https://docs.djangoproject.com/en/4.2/topics/db/queries/)

        Attributes:
            filter_by: a dictionary defining conditions a section should meet
            exclude: a dictionary defining conditions by which to exclude sections from selection
            song_ids: a list of identifiers of `Song` objects from which the section should be sampled

        Examples:
            >>> playlist.get_section(exclude={'group': 'Disney})
            West Side Story - America (0.0 - 10.0) OR West Side Story - America (30.0 - 40.0) OR
            Porgy and Bess - Summertime (0.0 - 10.0) OR Porgy and Bess - Summertime (30.0 - 40.0)

            >>> example_playlist.get_section({'tag': 'happy', 'start_time__gt': 20.0})
            West Side Story - America (30.0 - 40.0) OR Lion King - Hakuna Matata (30.0 - 40.0)

            >>> playlist.get_section(song_ids=[1])
            Frozen - Let It Go (0.0 - 10.0) OR Frozen - Let It Go (30.0 - 40.0)
        """
        if song_ids:
            sections = self.section_set.filter(song__id__in=song_ids)
        else:
            sections = self.section_set
        pks = (
            sections.exclude(**exclude).filter(**filter_by).values_list("pk", flat=True)
        )
        if len(pks) == 0:
            raise Section.DoesNotExist
        return self.section_set.get(pk=random.choice(pks))


class Song(models.Model):
    """A Song object with an artist and name, artist / name combinations must be unique

    Attributes:
        artist (str): the artist of a song
        name (str): the name of a song

    Examples:
        After adding the example playlist, the database would contain 4 Song objects
    """
    artist = models.CharField(db_index=True, blank=True, default='', max_length=128)
    name = models.CharField(db_index=True, blank=True, default='', max_length=128)

    class Meta:
        unique_together = ("artist", "name")


def _audio_upload_path(instance, filename: str) -> str:
    """Generate path to save audio based on playlist.name"""
    folder_name = instance.playlist.name.replace(" ", "")
    return join(folder_name, filename)


class Section(models.Model):
    """A snippet/section of a song, belonging to a Playlist

    Attributes:
        playlist (Playlist): a Many-To-One relationship to a Playlist object
        song (Song): a Many-To-One relationship to a Playlist object (can be null)
        start_time (float): the start time of the section in seconds, typically 0.0
        duration (float): the duration of the section in seconds, typically the duration of the audio file
        filename (str): the filename on the local file system or a link to an external file
        play_count (int): a counter for how often a given section has been played
        tag (str): a string with which to categorize the section
        group (str): another string with which to categorize the section

    Examples:
        After adding the example playlist, the database would contain 8 Section objects
    """

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.FloatField(db_index=True, default=0.0)  # start time in seconds
    duration = models.FloatField(default=0.0)  # end time in seconds
    filename = models.FileField(
        upload_to=_audio_upload_path,
        max_length=255,
        validators=[audio_file_validator()],
    )
    play_count = models.PositiveIntegerField(default=0)
    tag = models.CharField(max_length=128, default='0', blank=True)
    group = models.CharField(max_length=128, default='0', blank=True)

    class Meta:
        ordering = ['song__artist', 'song__name', 'start_time']

    def __str__(self):
        return f"{self.song_label()} ({self.start_time_str()}-{self.end_time_str()})"

    def artist_name(self, placeholder: str = "") -> str:
        """
        Attributes:
            placeholder: a placeholder in case the section does not have an associated Song

        Returns:
            artist of associated song or placeholder
        """
        if self.song:
            return self.song.artist
        else:
            return placeholder

    def song_name(self, placeholder: str = "") -> str:
        """
        Attributes:
            placeholder: a placeholder in case the section does not have an associated Song

        Returns:
            name of associated song or placeholder
        """
        if self.song:
            return self.song.name
        else:
            return placeholder

    def song_label(self) -> str:
        """
        Returns:
            formatted artist and name of associated song, if available
        """
        if self.artist_name() or self.song_name():
            return f"{self.artist_name()} - {self.song_name()}"
        return ""

    def start_time_str(self) -> str:
        """
        Returns:
            the start time in minutes:seconds.milliseconds format
        """
        return datetime.datetime.strftime(
            datetime.datetime.fromtimestamp(self.start_time), "%M:%S.%f"
        )[:-3]

    def end_time_str(self) -> str:
        """
        Returns:
            the end time in minutes:seconds.milliseconds format
        """
        return datetime.datetime.strftime(
            datetime.datetime.fromtimestamp(self.start_time + self.duration), "%M:%S.%f"
        )[:-3]

    def add_play_count(self):
        """Increase play count for this section"""
        self.play_count += 1

    def absolute_url(self) -> str:
        """
        Returns:
            a url consisting of the BASE_URL configured for Django, plus the filename
        """
        base_url = getattr(settings, 'BASE_URL', '')
        sections_url = reverse("section:section", args=[self.pk])
        return base_url.rstrip('/') + sections_url

    def _export_admin(self):
        """Export data for admin"""
        return {
            'id': self.id,
            'artist': self.song.artist,
            'name': self.song.name,
            'play_count': self.play_count
        }

    def _export_admin_csv(self):
        """Export csv data for admin"""
        return [
            self.song.artist,
            self.song.name,
            self.start_time,
            self.duration,
            self.filename,
            self.tag,
            self.group,
        ]
