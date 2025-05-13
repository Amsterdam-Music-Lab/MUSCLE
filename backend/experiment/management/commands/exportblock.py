import gzip
from os.path import join

from django.core.management.base import BaseCommand, CommandError

from experiment.models import Block
from experiment.utils import block_export_json_results


class Command(BaseCommand):
    """Command for exporting blocks using the manage.py script"""

    help = 'Export block data'

    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('block_slug',
                            type=str,
                            help="Block slug")
        parser.add_argument('directory', type=str, help="Directory to write to")

    def handle(self, *args, **options):
        block_slug = options['block_slug']
        directory = options['directory']
        try:
            block = Block.objects.get(slug=block_slug)
        except Block.DoesNotExist:
            raise CommandError(
                'Block "%s" does not exist with slug' % block_slug)

        zip_file = block_export_json_results(block_slug)
        with gzip.open(join(directory, f'{block_slug}.zip'), 'w+') as f:
            f.write(zip_file.getbuffer())
