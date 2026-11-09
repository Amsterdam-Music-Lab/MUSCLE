from django.test import TestCase

from action.models import Explainer, Final, Step
from experiment.actions.explainer import Explainer as ExplainerAction, Step as StepAction
from experiment.models import Block
from participant.models import Participant
from session.models import Session


class ExplainerText(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.explainer = Explainer.objects.create(
            identifier="test_explainer", instruction="Read this carefully!"
        )
        Step.objects.bulk_create(
            [
                Step(explainer=cls.explainer, description=f"Step {i}", index=i)
                for i in range(1, 5)
            ]
        )

    def test_step_convert_to_action(self):
        steps = Step.objects.all()
        first_step = steps.first().convert_to_action()
        self.assertIsInstance(first_step, StepAction)
        self.assertEqual(first_step.action()['description'], "<p>Step 1</p>")

    def test_explainer_convert_to_action(self):
        explainer_action = self.explainer.convert_to_action()
        self.assertIsInstance(explainer_action, ExplainerAction)
        self.assertEqual(
            explainer_action.action()["instruction"], "Read this carefully!"
        )


class FinalFeedbackTest(TestCase):
    fixtures = ["eurovision_2020"]

    def setUp(self):
        block = Block.objects.get(identifier="eurovision_2021")
        participant = Participant.objects.create()
        self.session = Session.objects.create(block=block, participant=participant)

    def test_feedback_final_score_condition(self):
        final = Final.objects.first()
        self.session.save_json_data({"final_score": 0})
        feedback_text = final.get_feedback_text(self.session)
        self.assertIn("Too bad!", feedback_text)
        self.session.save_json_data({"final_score": 1})
        feedback_text = final.get_feedback_text(self.session)
        self.assertIn("Well done!", feedback_text)

    def test_feedback_n_sync_condition(self):
        final = Final.objects.first()
        self.session.save_json_data({"n_sync_guessed": 0})
        feedback_text = final.get_feedback_text(self.session)
        self.assertIn("You did not recognise any songs at first.", feedback_text)
        self.session.save_json_data(
            {"n_sync_guessed": 20, "n_sync_correct": 10, 'mean_reaction_time': 4.2}
        )
        feedback_text = final.get_feedback_text(self.session)
        self.assertIn(
            "It took you 4.2 s to recognise a song on average, and you correctly identified 10 out of the 20 songs you thought you knew.",
            feedback_text,
        )
