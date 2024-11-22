from glob import glob
import csv
from os.path import basename, join, splitext
from os.path import split as pathsplit

import audioread
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from experiment.rules import BLOCK_RULES


class Command(BaseCommand):
    """Command for generating a csv to compile a playlist with sections
    Usage: python manage.py compileplaylist path/relative/to/upload/folder"""

    help = 'Generate a csv based on audio files in a directory'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('directory',
                            type=str,
                            help="Directory of audio files, relative to upload folder")
        parser.add_argument('--experiment',
                            type=str,
                            default=None,
                            help="Provide the ID of the experiment for which the playlist should be compiled")
        parser.add_argument('--artist_default',
                            type=str,
                            default='default',
                            help="Default name to assign to artist of sections")
        parser.add_argument('--tag_group',
                            type=str,
                            help='Process tags and groups for sections')
        parser.add_argument('--song_names',
                            type=str,
                            help='Read JSON file with song names for file names {<file-name>: <song-name>}')

    def handle(self, *args, **options):
        directory = options.get('directory')
        name = options.get('artist_default')
        upload_dir = settings.MEDIA_ROOT
        playlist_dir = join(upload_dir, directory)
        search_critera = glob('{}/*.wav'.format(playlist_dir)) + \
            glob('{}/*.mp3'.format(playlist_dir))
        song_names_option = options.get('song_names')
        if song_names_option:
            with open(join(playlist_dir, song_names_option)) as json_file:
                song_names = json.load(json_file)
        block_option = options.get('experiment')
        with open(join(playlist_dir, 'audiofiles.csv'), 'w+') as f:
            csv_writer = csv.writer(f)
            for i, audio_file in enumerate(search_critera):
                # set defaults
                artist_name = name
                song_name = name
                tag = group = '0'
                filename = join(directory, basename(audio_file))
                audio_file_clean = splitext(basename(audio_file))[0]
                if song_names_option:
                    artist_name = song_names[audio_file_clean]
                    song_name = basename(audio_file)[:-4]
                elif block_option:
                    rules = BLOCK_RULES.get(block_option)
                    info = rules.get_info_playlist(rules, audio_file_clean)
                    artist_name = info.get('artist')
                    song_name = info.get('song')
                    tag = info.get('tag')
                    group = info.get('group')
                else:
                    song_name = audio_file_clean
                start_position = 0.0
                with audioread.audio_open(audio_file) as f:
                    duration = f.duration
                group_tag_option = options.get('tag_group')
                if group_tag_option:
                    group, tag = calculate_group_tag(
                        filename, group_tag_option, i)
                row = [artist_name, song_name,
                       start_position, duration, filename,
                       tag, group]
                csv_writer.writerow(row)


def calculate_group_tag(filename, block, index):
    identifier = splitext(pathsplit(filename)[-1])[0]
    if block == 'huang2022':
        parts = identifier.split('.')
        group = parts[-1]
        tag = None
    else:
        parts = identifier.split('_')
    if block == 'hbat':
        # H-BAT style blocks:
        # level gets encoded as group
        # slower (1) or faster (0) gets encoded as tag
        group = int(parts[-1])
        tag = 1 if parts[-3] == 'S' else 0
    elif block == 'bst':
        # BST blocks:
        # level gets encoded as group
        # duple (1) / triple (0) gets encoded as tag
        group = int(parts[-1])
        tag = 1 if parts[-3] == 'D' else 0
    elif block == 'rhdi':
        # rhythm discrimination block:
        # standard (1) / deviant (0) gets encoded as group
        # tempo (160 - 200) gets encoded as tag
        group = 1 if parts[-2] == 'Standard' else 0
        tag = int(parts[-1])
    elif block == 'cat':
        # categorization block
        # Pair1: 1A, 1B / Pair2: 2A, 2B gets encodes as tag
        # Same direction: SAME, Crossed direction: CROSSED gets encoded as group
        if identifier[-2:] == '1A':
            tag = '1A'
        elif identifier[-2:] == '1B':
            tag = '1B'
        elif identifier[-2:] == '2A':
            tag = '2A'
        elif identifier[-2:] == '2B':
            tag = '2B'
        group = 'SAME' if identifier[0] == 'S' else 'CROSSED'
    elif block == 'matching_pairs':
        group = index
        tag = pathsplit(pathsplit(filename)[0])[1]
    return group, tag
