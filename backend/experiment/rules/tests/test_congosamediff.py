from unittest.mock import patch

from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from section.models import Playlist, Section, Song
from session.models import Session
from experiment.actions.explainer import Explainer
from experiment.actions.final import Final
from experiment.actions.trial import Trial
from experiment.rules.congosamediff import CongoSameDiff


class CongoSameDiffTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.section_csv = (
            "Dave,m1_contour_practice,0.0,20.0,samediff/melody_1_contour.wav,practice,1\n"
            "Dave,m2_same_practice,0.0,20.0,samediff/melody_1_same.wav,practice,1\n"
            "Dave,m1_same,0.0,20.0,samediff/melody_1_same.wav,A,1\n"
            "Dave,m1_scale,0.0,20.0,samediff/melody_1_scale.wav,B,1\n"
            "Dave,m1_contour,0.0,20.0,samediff/melody_1_contour.wav,C,1\n"
            "Dave,m1_interval,0.0,20.0,samediff/melody_1_interval.wav,D,1\n"
            "Dave,m2_same,0.0,20.0,samediff/melody_2_same.wav,A,2\n"
            "Dave,m2_scale,0.0,20.0,samediff/melody_2_scale.wav,B,2\n"
            "Dave,m2_contour,0.0,20.0,samediff/melody_2_contour.wav,C,2\n"
            "Dave,m2_interval,0.0,20.0,samediff/melody_2_interval.wav,D,2\n"
        )
        self.playlist = Playlist.objects.create(name='CongoSameDiff')
        self.playlist.csv = self.section_csv
        self.playlist._update_sections()
        self.participant = Participant.objects.create()
        self.block = Block.objects.create(
            slug="congosamediff", rules="CONGOSAMEDIFF", rounds=4
        )
        self.session = Session.objects.create(
            block=self.block,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        congo_same_diff = CongoSameDiff()
        assert congo_same_diff.ID == 'CONGOSAMEDIFF'
        assert congo_same_diff.contact_email == 'aml.tunetwins@gmail.com'

    def test_next_round_final_round(self):
        congo_same_diff = CongoSameDiff()

        Result.objects.create(
            session=self.session,
            participant=self.participant,
            question_key='practice_done',
            given_response='YES'
        )

        self.session.get_rounds_passed = lambda x: 2
        final_action = congo_same_diff.next_round(self.session)
        assert isinstance(final_action, Final)

    def test_next_round_practice_trial(self):
        congo_same_diff = CongoSameDiff()

        first_actions = congo_same_diff.next_round(self.session)
        self.assertEqual(len(first_actions), 2)
        self.assertIsInstance(first_actions[0], Explainer)

        practice_action = congo_same_diff.next_round(self.session)
        self.assertIsInstance(practice_action, Trial)
        self.assertEqual(
            practice_action.feedback_form.form[0].text,
            'Is the third sound the SAME or DIFFERENT as the first two sounds?',
        )

        next_action = congo_same_diff.next_round(self.session)
        self.assertIsInstance(next_action, Trial)
        self.assertEqual(
            next_action.feedback_form.form[0].text,
            'Did the participant complete the practice round correctly?',
        )

        # check that if there is no `practice_done` result with `given_answer=YES`, we get another practice round
        practice_action = congo_same_diff.next_round(self.session)
        self.assertIsInstance(practice_action, Trial)
        self.assertIn('PRACTICE', practice_action.feedback_form.form[0].key)

    def test_next_round_non_practice_trial(self):
        congo_same_diff = CongoSameDiff()
        Result.objects.create(
            session=self.session,
            participant=self.participant,
            question_key='practice_done',
            given_response='YES'
        )

        non_practice_action = congo_same_diff.next_round(self.session)
        self.assertIsInstance(non_practice_action, Trial)
        self.assertEqual(
            non_practice_action.feedback_form.form[0].text,
            'Is the third sound the SAME or DIFFERENT as the first two sounds?',
        )
        self.assertIn('NORMAL', non_practice_action.feedback_form.form[0].key)

    def test_get_next_trial(self):
        congo_same_diff = CongoSameDiff()
        subset = self.session.playlist.section_set.exclude(tag__contains='practice')
        trial_index = 1
        section = subset.all()[trial_index]
        is_practice = True
        trial_action = congo_same_diff.get_next_trial(self.session, section, trial_index, len(subset), is_practice)
        assert isinstance(trial_action, Trial)
        assert (
            trial_action.feedback_form.form[0].text
            == 'Is the third sound the SAME or DIFFERENT as the first two sounds?'
        )

    def test_get_final_round(self):
        congo_same_diff = CongoSameDiff()

        final_action = congo_same_diff.get_final_round(self.session)

        assert isinstance(final_action, Final)
        assert final_action.final_text == 'Thank you for participating!'

    def test_validate_playlist_trial_without_group(self):
        congo_same_diff = CongoSameDiff()
        playlist = Playlist.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='no_group', name='no_group'),
            tag='practice_contour',
            group=''
        )
        errors = congo_same_diff.validate_playlist(playlist)
        self.assertIn("Section no_group should have a group value containing only digits", errors)

    def test_validate_playlist_trial_group_not_int(self):
        congo_same_diff = CongoSameDiff()
        playlist = Playlist.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='group_not_int', name='group_not_int'),
            tag='practice_contour',
            group='not_int_42'
        )
        errors = congo_same_diff.validate_playlist(playlist)
        self.assertIn("Section group_not_int should have a group value containing only digits", errors)

    def test_validate_playlist_no_practice_rounds(self):
        congo_same_diff = CongoSameDiff()
        playlist = Playlist.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='no_practice', name='no_practice'),
            tag='',
            group='1'
        )
        errors = congo_same_diff.validate_playlist(playlist)
        self.assertIn('At least one section should have the tag "practice"', errors)

    def test_validate_playlist_no_normal_rounds(self):
        congo_same_diff = CongoSameDiff()
        playlist = Playlist.objects.create(name='CongoSameDiff')
        Section.objects.create(
            playlist=playlist,
            start_time=0.0,
            duration=20.0,
            song=Song.objects.create(artist='only_practice', name='only_practice'),
            tag='practice_contour',
            group='42'
        )
        errors = congo_same_diff.validate_playlist(playlist)
        self.assertIn('At least one section should not have the tag "practice"', errors)

    def test_validate_playlist_multiple_errors(self):
        congo_same_diff = CongoSameDiff()
        playlist = Playlist.objects.create(name='CongoSameDiff')
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
        errors = congo_same_diff.validate_playlist(playlist)
        self.assertIn('Section group_not_int should have a group value containing only digits', errors)
        self.assertIn('Section no_group should have a group value containing only digits', errors)
        self.assertIn('At least one section should not have the tag "practice"', errors)

    def test_get_total_trials_count(self):
        congo_same_diff = CongoSameDiff()
        total_trials_count = congo_same_diff.get_total_trials_count(self.session)
        assert total_trials_count == 2

    def test_get_participant_group_variant(self):
        csd = CongoSameDiff()
        groups = [1, 2]
        variants = ['A', 'B', 'C']

        # Test for participant 1 to 6 to match the expected sequence and reverses
        self.assertEqual(csd.get_participant_group_variant(0, 0, groups, variants), 'A')
        self.assertEqual(csd.get_participant_group_variant(0, 1, groups, variants), 'B')
        self.assertEqual(csd.get_participant_group_variant(0, 2, groups, variants), 'C')

        self.assertEqual(csd.get_participant_group_variant(1, 0, groups, variants), 'A')
        self.assertEqual(csd.get_participant_group_variant(1, 1, groups, variants), 'C')
        self.assertEqual(csd.get_participant_group_variant(1, 2, groups, variants), 'B')

        self.assertEqual(csd.get_participant_group_variant(2, 0, groups, variants), 'B')
        self.assertEqual(csd.get_participant_group_variant(2, 1, groups, variants), 'A')
        self.assertEqual(csd.get_participant_group_variant(2, 2, groups, variants), 'C')

        self.assertEqual(csd.get_participant_group_variant(3, 0, groups, variants), 'B')
        self.assertEqual(csd.get_participant_group_variant(3, 1, groups, variants), 'C')
        self.assertEqual(csd.get_participant_group_variant(3, 2, groups, variants), 'A')

        self.assertEqual(csd.get_participant_group_variant(4, 0, groups, variants), 'C')
        self.assertEqual(csd.get_participant_group_variant(4, 1, groups, variants), 'A')
        self.assertEqual(csd.get_participant_group_variant(4, 2, groups, variants), 'B')

        self.assertEqual(csd.get_participant_group_variant(5, 0, groups, variants), 'C')
        self.assertEqual(csd.get_participant_group_variant(5, 1, groups, variants), 'B')
        self.assertEqual(csd.get_participant_group_variant(5, 2, groups, variants), 'A')

        # test if participant #6 will get the first permutation again
        self.assertEqual(csd.get_participant_group_variant(6, 0, groups, variants), 'A')
        self.assertEqual(csd.get_participant_group_variant(6, 1, groups, variants), 'B')
        self.assertEqual(csd.get_participant_group_variant(6, 2, groups, variants), 'C')

    def test_edge_cases(self):
        congo_same_diff = CongoSameDiff()

        # Test edge cases
        self.assertEqual(congo_same_diff.get_participant_group_variant(0, 3, [1, 2, 3, 4], ['A', 'B', 'C']), 'A')  # Group number exceeds variants
        self.assertEqual(congo_same_diff.get_participant_group_variant(11, 0, [1, 2], ['A', 'B', 'C']), 'C')  # Reversed, with fewer groups than variants

    def test_invalid_parameters(self):
        congo_same_diff = CongoSameDiff()

        # Test scenarios with invalid parameters (should raise exceptions or handle gracefully)
        with self.assertRaises(ValueError):  # Assuming your method raises ValueError for invalid inputs
            congo_same_diff.get_participant_group_variant(-1, 1, [1, 2], ['A', 'B', 'C'])  # Negative participant ID
            congo_same_diff.get_participant_group_variant(1, -1, [1, 2], ['A', 'B', 'C'])  # Negative group number
            congo_same_diff.get_participant_group_variant(1, 1, [], ['A', 'B', 'C'])  # empty list of groups
            congo_same_diff.get_participant_group_variant(1, 1, [1, 2], [])  # empty list of tags
