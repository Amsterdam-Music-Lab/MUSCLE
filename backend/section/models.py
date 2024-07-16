import datetime
import random
import csv

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
    """List of sections to be used in an Experiment"""

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
        """Update playlist csv field on every save"""
        if self.process_csv is False and self.id:
            self.csv = self.update_admin_csv()
        if self.url_prefix and self.url_prefix[-1] != '/':
            self.url_prefix += '/'
        self.process_csv = False
        super(Playlist, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def section_count(self):
        """Number of sections"""
        return self.section_set.count()

    section_count.short_description = "Sections"

    def block_count(self):
        """Number of Blocks"""
        return self.block_set.count()

    block_count.short_description = "Blocks"

    def update_sections(self):
        """Update the sections from the csv file"""
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
        for row in reader:
            lines += 1

            # Check for valid row length in csv. If it has less than 8 entries, csv.DictReader will assign None to values of missing keys
            if None in row.values():
                return {
                    'status': self.CSV_ERROR,
                    'message': "Error: Invalid row length, line: " + str(lines)
                }

            # check for valid numbers
            if not (is_number(row['start_time'])
                    and is_number(row['duration'])):
                return {
                    'status': self.CSV_ERROR,
                    'message': "Error: Expected number fields on line: " + str(lines)
                }

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
            'message': "Sections processed from CSV. Added: " + str(len(sections)) + " - Updated: " + str(updated) + " - Removed: " + str(len(delete_ids))
        }

    def get_section(self, filter_by={}, song_ids=[]):
        """Get a random section from this playlist
            Optionally, limit to specific song_ids and filter conditions
        """
        if song_ids:
            sections = self.section_set.filter(song__id__in=song_ids)
        else:
            sections = self.section_set
        pks = sections.filter(**filter_by).values_list('pk', flat=True)
        if len(pks) == 0:
            raise Section.DoesNotExist
        return self.section_set.get(pk=random.choice(pks))

    def export_admin(self):
        """Export data for admin"""
        return {
            'exportedAt': timezone.now().isoformat(),
            'playlist': {
                'id': self.id,
                'name': self.name,
                'sections': [section.export_admin() for section in self.section_set.all()],
            },
        }

    def export_sections(self):
        # export section objects
        return self.section_set.all()

    def update_admin_csv(self):
        """Update csv data for admin"""
        csvfile = CsvStringBuilder()
        writer = csv.writer(csvfile)
        for section in self.section_set.all():
            if section.song:
                this_artist = section.song.artist
                this_name = section.song.name
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


class Song(models.Model):
    """ A Song object with an artist and name (unique together)"""
    artist = models.CharField(db_index=True, blank=True, default='', max_length=128)
    name = models.CharField(db_index=True, blank=True, default='', max_length=128)

    class Meta:
        unique_together = ("artist", "name")


def audio_upload_path(instance, filename):
    """Generate path to save audio based on playlist.name"""
    folder_name = instance.playlist.name.replace(' ', '')
    return '{0}/{1}'.format(folder_name, filename)


class Section(models.Model):
    """A snippet/section of a song, belonging to a Playlist"""

    def random_code():
        """Generate a random code for this section"""
        return random.randint(10000, 99999)

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.FloatField(db_index=True, default=0.0)  # sec
    duration = models.FloatField(default=0.0)  # sec
    filename = models.FileField(upload_to=audio_upload_path, max_length=255, validators=[audio_file_validator()])
    play_count = models.PositiveIntegerField(default=0)
    code = models.PositiveIntegerField(default=random_code)
    tag = models.CharField(max_length=128, default='0', blank=True)
    group = models.CharField(max_length=128, default='0', blank=True)

    class Meta:
        ordering = ['song__artist', 'song__name', 'start_time']

    def __str__(self):
        return "{} - {} ({}-{})".format(
            self.song.artist if self.song else '',
            self.song.name if self.song else '',
            self.start_time_str(),
            self.end_time_str()
        )

    def artist_name(self):
        if self.song:
            return self.song.artist
        else:
            return ''

    def song_name(self):
        if self.song:
            return self.song.name
        else:
            return ''

    def song_label(self):
        return "{} - {}".format(self.artist_name(), self.song_name())

    def start_time_str(self):
        """Create start time string 0:01:01.nn"""
        return str(datetime.timedelta(seconds=self.start_time)).rstrip('0')

    def end_time_str(self):
        """Create end time string 0:02:02.nn"""
        return str(datetime.timedelta(seconds=self.start_time + self.duration)).rstrip('0')

    def add_play_count(self):
        """Increase play count for this session"""
        self.play_count += 1

    def absolute_url(self):
        """Return absolute url for this section"""
        base_url = getattr(settings, 'BASE_URL', '')
        sections_url = reverse('section:section', args=[self.pk, self.code])
        return base_url.rstrip('/') + sections_url

    def simple_object(self):
        return {'id': self.id, 'url': self.absolute_url()}

    def export_admin(self):
        """Export data for admin"""
        return {
            'id': self.id,
            'artist': self.song.artist,
            'name': self.song.name,
            'play_count': self.play_count
        }

    def export_song(self):
        return self.instance

    def export_admin_csv(self):
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
