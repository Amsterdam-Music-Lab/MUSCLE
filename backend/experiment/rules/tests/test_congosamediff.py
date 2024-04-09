from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from section.models import Playlist as PlaylistModel, Section, Song
from session.models import Session
from experiment.actions import Explainer, Trial, Final, Playlist as PlaylistAction

from experiment.rules.congosamediff import CongoSameDiff


class CongoSameDiffTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.section_csv = (
            "Dave,m1_contour_practice,0.0,20.0,samediff/melody_1_contour.wav,practice,1\n"
            "Dave,m2_same_practice,0.0,20.0,samediff/melody_1_same.wav,practice,1\n"
            "Dave,m1_same,0.0,20.0,samediff/melody_1_same.wav,'',1\n"
            "Dave,m1_scale,0.0,20.0,samediff/melody_1_scale.wav,'',1\n"
            "Dave,m1_contour,0.0,20.0,samediff/melody_1_contour.wav,'',1\n"
            "Dave,m1_interval,0.0,20.0,samediff/melody_1_interval.wav,'',1\n"
            "Dave,m1_same,0.0,20.0,samediff/melody_1_same.wav,'',2\n"
            "Dave,m1_scale,0.0,20.0,samediff/melody_1_scale.wav,'',2\n"
            "Dave,m1_contour,0.0,20.0,samediff/melody_1_contour.wav,'',2\n"
            "Dave,m1_interval,0.0,20.0,samediff/melody_1_interval.wav,'',2\n"
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
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff_first_round', rounds=4)
        experiment.save()
        experiment.playlists.set([self.playlist])
        actions = congo_same_diff.first_round(experiment)
        assert len(actions) >= 1
        assert isinstance(actions[0], PlaylistAction)
        assert isinstance(actions[1], Explainer)

    def test_next_round_final_round(self):
        congo_same_diff = CongoSameDiff()

        Result.objects.create(
            session=self.session,
            participant=self.participant,
            question_key='practice_done',
            given_response='YES'
        )

        self.session.get_current_round = lambda: 6

        final_action = congo_same_diff.next_round(self.session)

        assert isinstance(final_action, Final)

    def test_next_round_practice_trial(self):
        congo_same_diff = CongoSameDiff()

        self.session.get_current_round = lambda: 2
        practice_action = congo_same_diff.next_round(self.session)

        assert isinstance(practice_action, Trial)
        assert practice_action.feedback_form.form[0].question == 'Is the third sound the SAME or DIFFERENT as the first two sounds?'

    def test_next_round_non_practice_trial(self):
        congo_same_diff = CongoSameDiff()

        self.session.get_current_round = lambda: 4
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

    def test_throw_exception_if_trial_without_group(self):
        congo_same_diff = CongoSameDiff()
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff_first_round', rounds=4)
        experiment.save()
        playlist = PlaylistModel.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='no_group', name='no_group'),
            tag='practice_contour',
            group=''
        )
        experiment.playlists.set([playlist])
        with self.assertRaisesRegex(ValueError, "Section no_group should have a group value"):
            congo_same_diff.first_round(experiment)

    def test_throw_exception_if_trial_group_not_int(self):
        congo_same_diff = CongoSameDiff()
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff_first_round', rounds=4)
        experiment.save()
        playlist = PlaylistModel.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='group_not_int', name='group_not_int'),
            tag='practice_contour',
            group='not_int_42'
        )
        experiment.playlists.set([playlist])
        with self.assertRaisesRegex(ValueError, "Section group_not_int should have a group value containing only digits"):
            congo_same_diff.first_round(experiment)

    def test_throw_exception_if_no_practice_rounds(self):
        congo_same_diff = CongoSameDiff()
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff_first_round', rounds=4)
        experiment.save()
        playlist = PlaylistModel.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='no_practice', name='no_practice'),
            tag='',
            group='1'
        )
        experiment.playlists.set([playlist])
        with self.assertRaisesRegex(ValueError, 'At least one section should have the tag "practice"'):
            congo_same_diff.first_round(experiment)

    def test_throw_exception_if_no_normal_rounds(self):
        congo_same_diff = CongoSameDiff()
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff_first_round', rounds=4)
        experiment.save()
        playlist = PlaylistModel.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='only_practice', name='only_practice'),
            tag='practice_contour',
            group='42'
        )
        experiment.playlists.set([playlist])
        with self.assertRaisesRegex(ValueError, 'At least one section should not have the tag "practice"'):
            congo_same_diff.first_round(experiment)

    def test_throw_combined_exceptions_if_multiple_errors(self):
        congo_same_diff = CongoSameDiff()
        experiment = Experiment(id=1, name='CongoSameDiff', slug='congosamediff_first_round', rounds=4)
        experiment.save()
        playlist = PlaylistModel.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='no_group', name='no_group'),
            tag='practice_contour',
            group=''
        )
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='group_not_int', name='group_not_int'),
            tag='practice_contour',
            group='not_int_42'
        )
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='only_practice', name='only_practice'),
            tag='practice_contour',
            group='42'
        )
        experiment.playlists.set([playlist])
        with self.assertRaisesRegex(ValueError, "The experiment playlist is not valid: \n- Section group_not_int should have a group value containing only digits\n- Section no_group should have a group value containing only digits\n- At least one section should not have the tag \"practice\""):
            congo_same_diff.first_round(experiment)

    def test_get_total_trials_count(self):
        congo_same_diff = CongoSameDiff()
        total_trials_count = congo_same_diff.get_total_trials_count(self.session)

        # practice trials + post-practice question + non-practice trials
        # 2 + 1 + 2 = 5
        assert total_trials_count == 5
