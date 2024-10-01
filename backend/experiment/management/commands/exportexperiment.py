import json
from django.core.management.base import BaseCommand, CommandError
from experiment.models import Block


class Command(BaseCommand):
    """Command for exporting blocks using the manage.py script"""

    help = 'Export block data'

    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('block_slug',
                            type=str,
                            help="Block slug")

        # Named (optional) arguments
        parser.add_argument(
            '--indent',
            type=int,
            default=0,
            help='JSON indent',
        )

    def handle(self, *args, **options):
        block_slug = options['block_slug']
        indent = options['indent']
        try:
            block = Block.objects.get(slug=block_slug)
        except Block.DoesNotExist:
            raise CommandError(
                'Block "%s" does not exist with slug' % block_slug)

        # Optional indent
        options = {}
        if indent > 0:
            options = {'indent': indent}

        self.stdout.write(json.dumps(block._export_admin(), **options))
