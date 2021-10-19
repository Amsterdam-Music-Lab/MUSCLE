import json
from django.core.management.base import BaseCommand, CommandError
from experiment.models import Experiment


class Command(BaseCommand):
    """Command for exporting experiments using the manage.py script"""

    help = 'Export experiment data'

    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('experiment_slug',
                            type=str,
                            help="Experiment slug")

        # Named (optional) arguments
        parser.add_argument(
            '--indent',
            type=int,
            default=0,
            help='JSON indent',
        )

    def handle(self, *args, **options):
        experiment_slug = options['experiment_slug']
        indent = options['indent']
        try:
            experiment = Experiment.objects.get(slug=experiment_slug)
        except Experiment.DoesNotExist:
            raise CommandError(
                'Experiment "%s" does not exist with slug' % experiment_slug)

        # Optional indent
        options = {}
        if indent > 0:
            options = {'indent': indent}

        self.stdout.write(json.dumps(experiment.export_admin(), **options))
