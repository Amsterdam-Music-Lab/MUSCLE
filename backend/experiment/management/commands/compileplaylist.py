from glob import glob
import csv
from os.path import basename, join, splitext
from os.path import split as pathsplit

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import audioread


class Command(BaseCommand):
    """Command for generating a csv to compile a playlist with sections
    Usage: python manage.py compileplaylist path/relative/to/upload/folder"""

    help = 'Generate a csv based on audio files in a directory'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('directory',
                            type=str,
                            help="Directory of audio files, relative to upload folder")
        parser.add_argument('--artist_default',
                            type=str,
                            default='default',
                            help="Default name to assign to artist of sections")
        parser.add_argument('--tag_group',
                            type=str,
                            help='Process tags and groups for sections')

    def handle(self, *args, **options):
        directory = options.get('directory')
        name = options.get('artist_default')

        upload_dir = settings.MEDIA_ROOT
        playlist_dir = join(upload_dir, directory)
        search_critera = glob('{}/*.wav'.format(playlist_dir)) + glob('{}/*.mp3'.format(playlist_dir))
        with open(join(playlist_dir, 'audiofiles.csv'), 'w+') as f:
            csv_writer = csv.writer(f)
            for audio_file in search_critera:
                artist_name = name
                filename = join(directory,basename(audio_file))
                song_name = splitext(basename(audio_file))[0]
                start_position = 0.0
                with audioread.audio_open(audio_file) as f:
                    duration = f.duration
                restrict_to_nl = 0
                group_tag_option = options.get('tag_group')
                if group_tag_option:
                    group_id, tag_id = calculate_group_tag(filename, group_tag_option)
                else:
                    group_id = tag_id = 0
                row = [artist_name, song_name,
                    start_position, duration, filename, restrict_to_nl,
                    tag_id, group_id]
                csv_writer.writerow(row)


def calculate_group_tag(filename, experiment):
    identifier = splitext(pathsplit(filename)[-1])[0]
    parts = identifier.split('_')
    if experiment == 'hbat':
        # H-BAT style experiments:
        # level gets encoded as group
        # slower (1) or faster (0) gets encoded as tag
        group = int(parts[-1])
        tag = 1 if parts[-3] == 'S' else 0
    elif experiment == 'bst':
        # BST experiments:
        # level gets encoded as group
        # duple (1) / triple (0) gets encoded as tag
        group = int(parts[-1])
        tag = 1 if parts[-3] == 'D' else 0
    elif experiment == 'rhdi':
        # rhythm discrimination experiment:
        # standard (1) / deviant (0) gets encoded as group
        # tempo (160 - 200) gets encoded as tag
        group = 1 if parts[-2] == 'Standard' else 0
        tag = int(parts[-1])
    return group, tag







