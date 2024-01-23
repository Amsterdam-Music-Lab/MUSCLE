from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from experiment.models import Experiment
from section.models import Playlist


class Command(BaseCommand):
    """ Command for creating a superuser and an experiment if they do not yet exist """

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            management.call_command('createsuperuser', '--no-input')
            print('Created superuser')
        if Experiment.objects.count() == 0:
            playlist = Playlist.objects.create(
                name='Empty Playlist'
            )
            experiment = Experiment.objects.create(
                name='Goldsmiths Musical Sophistication Index',
                rules='GOLD_MSI',
                slug='gold-msi',
            )
            experiment.playlists.add(playlist)
            print('Created default experiment')

