import csv
import random
from django.utils import timezone
from django.db import models


class Playlist(models.Model):
    """List of sections to be used in an Experiment"""

    name = models.CharField(db_index=True, max_length=64)

    process_warning = 'Warning: Processing a live playlist may affect the result data'
    process_csv = models.BooleanField(default=False, help_text=process_warning)

    default_csv_row = 'CSV Format: artist_name [string],\
        song_name [string], start_position [float], duration [float],\
        "path/filename.mp3" [string], restricted_to_nl [int 0=False 1=True], tag [string], group [string]'
    csv = models.TextField(blank=True, help_text=default_csv_row)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def section_count(self):
        """Number of sections"""
        return self.section_set.count()

    section_count.short_description = "Sections"

    def experiment_count(self):
        """Number of Experiments"""
        return self.experiment_set.count()

    experiment_count.short_description = "Experiments"

    CSV_OK = 0
    CSV_ERROR = 10

    def update_sections(self):
        """Update the sections from the csv file"""

        # Import sections here to prevent circular dependency errors
        # pylint: disable=import-outside-toplevel
        from . import Section

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
                'artist', 'name', 'start_time', 'duration', 'filename', 'restrict_to_nl', 'tag', 'group'))
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
                    and is_number(row['duration'])
                    and is_number(row['restrict_to_nl'])):
                return {
                    'status': self.CSV_ERROR,
                    'message': "Error: Expected number fields on line: " + str(lines)
                }

            # create new section
            section = Section(playlist=self,
                              artist=row['artist'],
                              name=row['name'],
                              start_time=float(row['start_time']),
                              duration=float(row['duration']),
                              filename=row['filename'],
                              restrict_to_nl=(int(row['restrict_to_nl']) == 1),
                              tag=row['tag'],
                              group=row['group'],
                              )

            # if same section already exists, update it with new info
            for ex_section in existing_sections:
                if (ex_section.artist == section.artist
                    and ex_section.name == section.name
                    and ex_section.start_time - section.start_time == 0
                    and ex_section.duration == section.duration
                    and ex_section.tag == section.tag
                        and ex_section.group == section.group):

                    # Update if necessary
                    if ex_section.filename != section.filename or ex_section.restrict_to_nl != section.restrict_to_nl:
                        ex_section.filename = section.filename
                        ex_section.restrict_to_nl = section.restrict_to_nl
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

        return {
            'status': self.CSV_OK,
            'message': "Sections processed from CSV. Added: " + str(len(sections)) + " - Updated: " + str(updated) + " - Removed: " + str(len(delete_ids))
        }

    def song_ids(self, filter_by={}):
        """Get a list of distinct song ids"""
        # order_by is required to make distinct work with values_list
        return self.section_set.filter(**filter_by).order_by('pk').values_list('pk', flat=True).distinct()

    def random_section(self, filter_by={}):
        """Get a random section from this playlist"""
        pks = self.section_set.filter(**filter_by).values_list('pk', flat=True)
        if len(pks) == 0:
            return None
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
