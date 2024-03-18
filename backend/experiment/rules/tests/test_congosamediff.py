from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist as PlaylistModel, Section, Song
from session.models import Session
from experiment.actions import Explainer, Trial, Final, Playlist as PlaylistAction

from experiment.rules.congosamediff import CongoSameDiff


class CongoSameDiffTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.section_csv = (
            "Dave,m1_contour,0.0,20.0,samediff/melody_1_contour.wav,practice_contour,m1\n"
            "Dave,m1_interval,0.0,20.0,samediff/melody_1_interval.wav,practice_interval,m1\n"
            "Dave,m1_same,0.0,20.0,samediff/melody_1_same.wav,same,m1\n"
            "Dave,m1_scale,0.0,20.0,samediff/melody_1_scale.wav,scale,m1\n"
        )
        self.playlist = PlaylistModel.objects.create(name='CongoSameDiff')
        self.playlist.csv = self.section_csv
        self.playlist.update_sections()
        self.participant = Participant.objects.create()
        self.experiment = Experiment.objects.create(
            name='CongoSameDiff',
            slug='congosamediff',
            rounds=4,
        )
        self.session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        congo_same_diff = CongoSameDiff()
        assert congo_same_diff.ID == 'CONGOSAMEDIFF'
        assert congo_same_diff.contact_email == 'aml.tunetwins@gmail.com'

    def test_first_round(self):
        congo_same_diff = CongoSameDiff()
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff', rounds=4)
        actions = congo_same_diff.first_round(experiment)
        assert len(actions) >= 1
        assert isinstance(actions[0], PlaylistAction)
        assert isinstance(actions[1], Explainer)

    def test_next_round_final_round(self):
        congo_same_diff = CongoSameDiff()

        self.session.get_next_round = lambda: 6
        final_action = congo_same_diff.next_round(self.session)

        assert isinstance(final_action, Final)

    def test_next_round_practice_trial(self):
        congo_same_diff = CongoSameDiff()

        self.session.get_next_round = lambda: 2
        practice_action = congo_same_diff.next_round(self.session)

        assert isinstance(practice_action, Trial)
        assert practice_action.feedback_form.form[0].question == 'Is the third sound the SAME or DIFFERENT as the first two sounds?'

    def test_next_round_non_practice_trial(self):
        congo_same_diff = CongoSameDiff()

        self.session.get_next_round = lambda: 4
        non_practice_action = congo_same_diff.next_round(self.session)

        assert isinstance(non_practice_action, Trial)
        assert non_practice_action.feedback_form.form[0].question == 'Is the third sound the SAME or DIFFERENT as the first two sounds?'

    def test_get_next_trial(self):
        congo_same_diff = CongoSameDiff()
        subset = self.session.playlist.section_set.exclude(tag__contains='practice')
        trial_index = 1
        is_practice = True
        trial_action = congo_same_diff.get_next_trial(self.session, subset, trial_index, is_practice)
        assert isinstance(trial_action, Trial)
        assert trial_action.feedback_form.form[0].question == 'Is the third sound the SAME or DIFFERENT as the first two sounds?'

    def test_get_final_round(self):
        congo_same_diff = CongoSameDiff()

        final_action = congo_same_diff.get_final_round(self.session)

        assert isinstance(final_action, Final)
        assert final_action.final_text == 'Thank you for participating!'


