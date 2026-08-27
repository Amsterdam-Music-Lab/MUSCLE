from django.test import TestCase

from experiment.models import Block, Phase
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session

from experiment.actions.explainer import Explainer
from experiment.actions.final import Final
from experiment.actions.trial import Trial
from experiment.rules.speech2song import sound, Speech2Song
from experiment.serializers import serialize_actions


class Speech2SongTest(TestCase):
    fixtures = ["choice_lists", "demographics", "speech2song"]

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.get(name='Speech2Song')
        cls.playlist._update_sections()
        cls.participant = Participant.objects.create()
        cls.block = Block.objects.get(
            identifier='s2s',
        )
        cls.block.rounds = 16
        cls.block.save()
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )

    def test_sound_method(self):
        section = self.playlist.section_set.first()
        view = sound(section)
        self.assertEqual(type(view), Trial)

    def test_single_presentation(self):
        group = self.playlist.section_set.first().group
        actions = self.session.block_rules().next_single_representation(self.session, True, int(group))
        self.assertEqual(type(actions), list)

    def test_repeated_presentation(self):
        section = self.playlist.section_set.first()
        Result.objects.create(
            question_identifier='speech2song',
            session=self.session,
            section=section,
            score=2,
        )
        actions = self.session.block_rules().next_repeated_representation(self.session, True)
        self.assertEqual(type(actions), list)

    def test_next_round(self):
        speech2song = Speech2Song()
        actions = speech2song.next_round(self.session)
        self.assertEqual(type(actions), list)

    def test_next_round_serialization(self):
        speech2song = Speech2Song()
        actions = speech2song.next_round(self.session)
        serialized = serialize_actions(actions)
        self.assertEqual(type(serialized), list)
        for s in serialized:
            self.assertEqual(type(s), dict)

    def test_runthrough(self):
        speech2song = self.session.block_rules()
        self.block.questionlist_set.all().delete()  # delete the questions so we get straight to speech2song trials
        speech2song.n_trials_per_block = 2
        for i in range(self.block.rounds - 1):
            actions = speech2song.next_round(self.session)
            feedback_trial = next((a for a in actions if a.__dict__.get('feedback_form')))
            result = Result.objects.get(pk=feedback_trial.feedback_form.form[0].result_id)
            result.score = 42
            result.save()
            if i == 0:
                self.assertEqual(self._number_of_sound_trials(actions), speech2song.n_presentations)
            elif i == 1:
                self.assertIsInstance(actions[0], Explainer)
                self.assertEqual(self._number_of_sound_trials(actions), 1)
            elif i == self.block.rounds - 1:
                self.assertIsInstance(actions[0], Final)
            elif i == speech2song.n_trials_per_block * 2 * 3 + 1:
                self.assertIsInstance(actions[0], Explainer)
            elif i % 2 == 0:
                self.assertEqual(self._number_of_sound_trials(actions), speech2song.n_presentations)
            elif i % 2 == 1:
                self.assertEqual(self._number_of_sound_trials(actions), 1)

    def _number_of_sound_trials(self, actions):
        sound_actions = [a for a in actions if a.__dict__.get('playback')]
        return len(sound_actions)
