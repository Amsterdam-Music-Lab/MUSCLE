from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from experiment.models import Block, Experiment, Phase
from section.models import Playlist
from question.questions import create_default_questions


class Command(BaseCommand):
    """Command for creating a superuser and a block if they do not yet exist"""

    def handle(self, *args, **options):
        create_default_questions()

        if User.objects.count() == 0:
            management.call_command("createsuperuser", "--no-input")
            print("Created superuser")
        if Experiment.objects.count() == 0:
            experiment = Experiment.objects.create(slug="test")
            phase = Phase.objects.create(experiment=experiment)
            playlist = Playlist.objects.create(name="Empty Playlist")
            block = Block.objects.create(
                phase=phase,
                rules="RHYTHM_BATTERY_FINAL",
                slug="gold-msi",
            )
            block.playlists.add(playlist)
            block.add_default_question_series()
            print("Created default experiment, phase and block")
