from django.test import TestCase

from experiment.models import Experiment
from experiment.rules import HBat, BST
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session

class HBatTest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='HBAT-BIT')
        cls.playlist.update_sections()
        cls.experiment = Experiment.objects.get(name='HBAT-BIT')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=cls.playlist
        )
    
    def test_trial_action(self):
        level = 4
        slower_trial = HBat.next_trial_action(self.session, 1, level)
        assert slower_trial
        result_id = slower_trial.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == 'SLOWER'
        faster_trial = HBat.next_trial_action(self.session, 0, level)
        assert faster_trial
        result_id = faster_trial.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == 'FASTER'

class HBat_BST_Test(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='HBAT-BST')
        cls.playlist.update_sections()
        cls.experiment = Experiment.objects.get(name='HBAT-BST')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=cls.playlist
        )
    
    def test_trial_action(self):
        in2 = BST.next_trial_action(self.session, 1, 3)
        assert in2
        result_id = in2.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == 'in2'
        in3 = BST.next_trial_action(self.session, 0, 3)
        assert in3
        result_id = in3.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == 'in3'