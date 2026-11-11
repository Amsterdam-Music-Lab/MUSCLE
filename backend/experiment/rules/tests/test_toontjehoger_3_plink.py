from django.test import TestCase

from experiment.models import Block
from experiment.rules.toontjehoger_3_plink import ToontjeHoger3Plink
from experiment.rules.toontjehogerkids_3_plink import ToontjeHogerKids3Plink
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session


class TestToontjeHoger3Plink(TestCase):
    fixtures = ["toontjehoger"]

    def test_initializes(self):
        rules = ToontjeHoger3Plink()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_3_PLINK")

    def test_can_play_through(self):
        playlist = Playlist.objects.get(name="Toontje Hoger 3 - Plink")
        playlist._update_sections()
        block = Block.objects.get(identifier="th_plink")
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            actions = rules.next_round(session)
            last_result = session.result_set.filter(question_identifier='plink').last()
            last_result.score = rules.SCORE_MAIN_CORRECT
            last_result.save()
            self.assertIsNotNone(actions)

    def test_calculate_score(self):
        block = Block.objects.get(identifier="th_plink")
        playlist = Playlist.objects.get(name="Toontje Hoger 3 - Plink")
        playlist._update_sections()
        session = Session.objects.create(
            block=block, participant=Participant.objects.create(), playlist=playlist
        )
        rules = block.get_rules()
        result = Result.objects.create(
            question_identifier="plink",
            session=session,
            expected_response=playlist.section_set.first().pk,
            given_response=str(playlist.section_set.first().pk),
        )
        score = rules.calculate_score(result, {})
        self.assertEqual(score, rules.SCORE_MAIN_CORRECT)
        result.given_response = str(playlist.section_set.last().pk)
        score = rules.calculate_score(result, {})
        self.assertEqual(score, rules.SCORE_MAIN_WRONG)
        result = Result.objects.create(
            question_identifier="era",
            session=session,
            expected_response="80s",
            given_response="80s",
        )
        score = rules.calculate_score(result, {})
        self.assertEqual(score, rules.SCORE_EXTRA_1_CORRECT)
        result = Result.objects.create(
            question_identifier="mood",
            session=session,
            expected_response="vrolijk",
            given_response="vrolijk",
        )
        score = rules.calculate_score(result, {})
        self.assertEqual(score, rules.SCORE_EXTRA_2_CORRECT)

    def test_get_last_results(self):
        block = Block.objects.get(identifier="th_plink")
        playlist = Playlist.objects.get(name="Toontje Hoger 3 - Plink")
        playlist._update_sections()
        session = Session.objects.create(
            block=block, participant=Participant.objects.create(), playlist=playlist
        )
        rules = block.get_rules()
        plink_result = Result.objects.create(
            question_identifier="plink",
            session=session,
            expected_response=playlist.section_set.first().pk,
            given_response=playlist.section_set.first().pk + 1,
        )
        self.create_extra_results(session)
        results = rules.get_last_results(session)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].question_identifier, "plink")
        plink_result.given_response = "SKIPPED"
        plink_result.save()
        self.create_extra_results(session)
        results = rules.get_last_results(session)
        self.assertEqual(len(results), 2)
        question_ids = [r.question_identifier for r in results]
        self.assertIn("era", question_ids)
        self.assertIn("mood", question_ids)

    def create_extra_results(self, session: Session):
        Result.objects.create(
            question_identifier="mood",
            session=session,
            expected_response="vrolijk",
            given_response="droevig",
        )
        Result.objects.create(
            question_identifier="era",
            session=session,
            expected_response="20s",
            given_response="10s",
        )


class TestToontjeHogerKids3Plink(TestCase):
    fixtures = ["toontjehoger_kids"]

    def test_initializes(self):
        rules = ToontjeHogerKids3Plink()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_3_PLINK")

    def test_can_play_through(self):
        playlist = Playlist.objects.get(name="THK_Plink")
        playlist._update_sections()
        block = Block.objects.get(identifier="thk_plink")
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))
