from django.test import TestCase

from experiment.models import Experiment
from experiment.rules import Anisochrony, DurationDiscrimination
from participant.models import Participant
from section.models import Playlist, Section
from session.models import Session

class DDITest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='DurationDiscrimination')
        cls.playlist.update_sections()
        cls.experiment = Experiment.objects.get(name='DurationDiscrimination')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.session.experiment_rules()

    def test_trial_action(self):
        difference = 200000
        catch_section = Section.objects.get(playlist=self.playlist.id, song__name=0)
        diff_section = Section.objects.get(playlist=self.playlist.id, song__name=difference)
        catch_trial = self.rules.next_trial_action(self.session, 1, difference)
        assert catch_trial
        assert catch_trial.feedback_form
        section = catch_trial.playback.sections[0]
        assert section['id'] == catch_section.id
        regular_trial = self.rules.next_trial_action(self.session, 0, difference)
        assert regular_trial
        assert regular_trial.feedback_form
        section = regular_trial.playback.sections[0]
        assert section['id'] == diff_section.id

class AnisochronyTest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='Anisochrony')
        cls.playlist.update_sections()
        cls.experiment = Experiment.objects.get(name='Anisochrony')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.session.experiment_rules()
    
    def test_trial_action(self):
        difficulty = 1001
        catch_section = Section.objects.get(playlist=self.playlist.id, song__name=0)
        diff_section = Section.objects.get(playlist=self.playlist.id, song__name=difficulty)
        catch_trial = self.rules.next_trial_action(self.session, 1, difficulty)
        assert catch_trial
        assert catch_trial.feedback_form
        section = catch_trial.playback.sections[0]
        assert section['id'] == catch_section.id
        regular_trial = self.rules.next_trial_action(self.session, 0, difficulty)
        assert regular_trial
        assert regular_trial.feedback_form
        section = regular_trial.playback.sections[0]
        assert section['id'] == diff_section.id
