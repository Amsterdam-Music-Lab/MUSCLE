import csv
from os.path import join
from os import remove

from django.core.management import call_command
from django.test import TestCase
from django.conf import settings

from experiment.models import Block, Experiment, Phase
from section.models import Playlist

class CompilePlaylistTest(TestCase):

    def test_output_csv(self):
        call_command('compileplaylist', 'tests/compileplaylist')
        # Load generated csv
        filename = join(settings.MEDIA_ROOT,'tests','compileplaylist','audiofiles.csv')
        try:
            with open(filename) as csv_file:
                rows = csv.DictReader(csv_file, fieldnames = ('artist','name','start_time','duration','filename','tag','group'))
                for row in rows:
                    if row['filename'] == 'tests/compileplaylist/silence_20sec.wav':
                        self.assertEqual(row['artist'], 'default')
                        self.assertEqual(row['name'], 'silence_20sec')
                        self.assertEqual(row['start_time'], '0.0')
                        self.assertEqual(row['duration'], '20.025850340136053')
                        self.assertEqual(row['tag'], '0')
                        self.assertEqual(row['group'], '0')
        finally:
            remove(filename)  # Make sure csv file is deleted even if tests fail


class BootrapTest(TestCase):

    def test_bootstrap(self):
        call_command("bootstrap")
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Phase.objects.count(), 1)
        self.assertEqual(Block.objects.count(), 1)
        self.assertEqual(Playlist.objects.count(), 1)
