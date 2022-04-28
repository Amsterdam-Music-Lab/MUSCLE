import datetime
import random
from django.db import models
from django.urls import reverse
from . import Playlist


class Section(models.Model):
    """A snippet/section of a song, belonging to a Playlist"""

    def random_code():
        """Generate a random code for this section"""
        return random.randint(10000, 99999)

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    artist = models.CharField(db_index=True, max_length=128)
    name = models.CharField(db_index=True, max_length=128)
    start_time = models.FloatField(db_index=True, default=0.0)  # sec
    duration = models.FloatField(default=0.0)  # sec
    filename = models.CharField(max_length=128)
    restrict_to_nl = models.BooleanField(default=False)
    play_count = models.PositiveIntegerField(default=0)
    code = models.PositiveIntegerField(default=random_code)
    tag_id = models.CharField(max_length=128, default='0')
    group_id = models.CharField(max_length=128, default='0')

    class Meta:
        ordering = ['artist', 'name', 'start_time']

    def __str__(self):
        return "{} - {} ({}-{})".format(
            self.artist,
            self.name,
            self.start_time_str(),
            self.end_time_str()
        )

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
        return reverse('experiment:section', args=[self.pk, self.code])

    def export_admin(self):
        """Export data for admin"""
        return {
            'id': self.id,
            'artist': self.artist,
            'name': self.name,
            'play_count': self.play_count
        }

    def export_admin_csv(self):
        """Export csv data for admin"""
        return [
            self.id,
            self.pk,
            self.artist,
            self.name,
            self.start_time,
            self.duration,
            self.filename,
            1 if self.restrict_to_nl else 0,
            self.play_count,
            self.tag_id,
            self.group_id,
        ]
