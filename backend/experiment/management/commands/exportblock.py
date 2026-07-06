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
        parser.add_argument('block_identifier', type=str, help="Block identifier")
        parser.add_argument('directory', type=str, help="Directory to write to")

    def handle(self, *args, **options):
        block_identifier = options['block_identifier']
        directory = options['directory']
        try:
            Block.objects.get(identifier=block_identifier)
        except Block.DoesNotExist:
            raise CommandError(
                'Block "%s" does not exist with identifier' % block_identifier
            )

        zip_file = block_export_json_results(block_identifier)
        with gzip.open(join(directory, f'{block_identifier}.zip'), 'w+') as f:
            f.write(zip_file.getbuffer())
