from django.test import TestCase

from experiment.models import Block
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
        cls.playlist._update_sections()
        cls.block = Block.objects.get(slug="hbat_bit")
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.session.block_rules()

    def test_get_next_trial(self):
        self.session.save_json_data({"conditions": ["slower"]})
        slower_trial = self.rules.get_next_trial(self.session)
        assert slower_trial
        result_id = slower_trial.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == "slower"
        self.session.save_json_data({"conditions": ["faster"]})
        faster_trial = self.rules.get_next_trial(self.session)
        assert faster_trial
        result_id = faster_trial.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == "faster"


class HBat_BST_Test(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='HBAT-BST')
        cls.playlist._update_sections()
        cls.block = Block.objects.get(slug="hbat_bst")
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.session.block_rules()

    def test_trial_action(self):
        self.session.save_json_data({"conditions": ["in2"]})
        in2 = self.rules.get_next_trial(self.session)
        assert in2
        result_id = in2.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == 'in2'
        self.session.save_json_data({"conditions": ["in3"]})
        in3 = self.rules.get_next_trial(self.session)
        assert in3
        result_id = in3.feedback_form.form[0].result_id
        result = Result.objects.get(pk=result_id)
        assert result
        assert result.expected_response == 'in3'
