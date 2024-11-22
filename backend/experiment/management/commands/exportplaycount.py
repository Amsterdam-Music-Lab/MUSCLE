import json
from django.core.management.base import BaseCommand, CommandError
from experiment.models import Playlist


class Command(BaseCommand):
    """Command for exporting section playcount using the manage.py script"""

    help = 'Export section playcount'

    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('playlist_id',
                            type=int,
                            help="Playlist id")

        # Named (optional) arguments
        parser.add_argument(
            '--indent',
            type=int,
            default=0,
            help='JSON indent',
        )

    def handle(self, *args, **options):
        playlist_id = options['playlist_id']
        indent = options['indent']
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            raise CommandError(
                'Playlist "%s" does not exist with pk' % playlist_id)

        # Optional indent
        options = {}
        if indent > 0:
            options = {'indent': indent}

        self.stdout.write(json.dumps(playlist._export_admin(), **options))
