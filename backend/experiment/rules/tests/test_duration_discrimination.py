import random
from unittest import skip

from django.test import TestCase

from experiment.actions import Explainer, Final, Trial
from experiment.models import Block
from participant.models import Participant
from result.models import Result
from section.models import Playlist, Section
from session.models import Session


class DDITest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='DurationDiscrimination')
        cls.playlist._update_sections()
        cls.block = Block.objects.get(slug="ddi")
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.session.block_rules()

    def test_practice_rounds(self):
        actions = self.block.get_rules().next_round(self.session)
        self.assertEqual(len(actions), 3)
        self.assertIsInstance(actions[0], Explainer)
        self.assertIsInstance(actions[1], Explainer)
        self.assertIsInstance(actions[2], Trial)
        for i in range(3):
            self.populate_result_score(self.session, 0)
            actions = self.block.get_rules().next_round(self.session)
            self.assertEqual(len(actions), 2)
            self.assertIsInstance(actions[0], Explainer)
            self.assertIsInstance(actions[1], Trial)
        self.populate_result_score(self.session, 1)
        # practice failed, we get the same actions as in round 0, plus 2 more explainers
        self.assertIsNone(self.session.json_data.get("practice_done"))
        actions = self.block.get_rules().next_round(self.session)
        self.assertEqual(len(actions), 5)
        for i in range(4):
            self.assertIsInstance(actions[i], Explainer)
        self.assertIsInstance(actions[4], Trial)
        for i in range(3):
            actions = self.block.get_rules().next_round(self.session)
            self.populate_result_score(self.session, 1)
            self.assertEqual(len(actions), 2)
            self.assertIsInstance(actions[0], Explainer)
            self.assertIsInstance(actions[1], Trial)
        self.populate_result_score(self.session, 1)
        actions = self.block.get_rules().next_round(self.session)
        # practice succeeded
        self.assertTrue(self.session.json_data.get("practice_done"))

    def populate_result_score(self, session: Session, score: int):
        result = session.last_result()
        result.score = score
        result.save()

    def test_get_next_trial(self):
        Result.objects.create(session=self.session)
        difference = 200000
        catch_section = Section.objects.get(playlist=self.playlist.id, song__name=0)
        diff_section = Section.objects.get(playlist=self.playlist.id, song__name=difference)
        self.session.save_json_data(
            {
                "practice_done": True,
                "difficulty": difference,
                "current_trials": ["equal"],
            }
        )
        catch_trial = self.rules.get_next_trial(self.session)
        assert catch_trial
        assert catch_trial.feedback_form
        section = catch_trial.playback.sections[0]
        assert section['id'] == catch_section.id
        self.session.save_json_data({"current_trials": ["longer"]})
        regular_trial = self.rules.get_next_trial(self.session)
        assert regular_trial
        assert regular_trial.feedback_form
        section = regular_trial.playback.sections[0]
        assert section['id'] == diff_section.id

    @skip(
        "This test simulates playing through the whole experiment, uncomment this line to run"
    )
    def test_simulate_full_experiment(self):
        n_games = 20
        self.session.save_json_data(
            {"practice_done": True, "difficulty": self.rules.start_diff}
        )
        for game in range(n_games):
            for round_number in range(50):
                print(f"Round {round_number+1} of game {game+1}")
                actions = self.rules.next_round(self.session)
                self.assertIsNotNone(actions)
                if isinstance(actions, Trial):
                    last_result = Result.objects.last()
                    if last_result.expected_response == 'longer':
                        last_result.score = random.choice([0, 1])
                    else:
                        last_result.score = random.choice([0, 2])
                    last_result.save()
                else:
                    Result.objects.all().delete()
                    self.session.final_score = 0
                    self.session.save_json_data({"difficulty": self.rules.start_diff})
                    self.assertIsInstance(actions, Final)
                    break


class AnisochronyTest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='Anisochrony')
        cls.playlist._update_sections()
        cls.block = Block.objects.get(slug="anis")
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.session.block_rules()

    def test_trial_action(self):
        Result.objects.create(session=self.session)
        catch_section = Section.objects.get(playlist=self.playlist.id, song__name=0)
        self.session.save_json_data(
            {"current_trials": ["regular"], "practice_done": True}
        )
        catch_trial = self.rules.get_next_trial(self.session)
        assert catch_trial
        assert catch_trial.feedback_form
        section = catch_trial.playback.sections[0]
        assert section["id"] == catch_section.id
        difficulty = 1001
        self.session.save_json_data(
            {"current_trials": ["irregular"], "difficulty": difficulty}
        )
        diff_section = Section.objects.get(
            playlist=self.playlist.id, song__name=difficulty
        )
        regular_trial = self.rules.get_next_trial(self.session)
        assert regular_trial
        assert regular_trial.feedback_form
        section = regular_trial.playback.sections[0]
        assert section['id'] == diff_section.id
