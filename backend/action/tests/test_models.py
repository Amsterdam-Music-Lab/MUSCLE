from django.test import TestCase

from action.models import Explainer, Step
from experiment.actions.explainer import Explainer as ExplainerAction, Step as StepAction

class TestExplainer(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.explainer = Explainer.objects.create(identifier="test_explainer", instruction="Read this carefully!")
        Step.objects.bulk_create([Step(explainer=cls.explainer, description=f"Step {i}", index=i) for i in range(1, 5)])

    def test_step_convert_to_action(self):
        steps = Step.objects.all()
        first_step = steps.first().convert_to_action()
        self.assertIsInstance(first_step, StepAction)
        self.assertEqual(first_step.action()['description'], "<p>Step 1</p>")
    
    def test_explainer_convert_to_action(self):
        explainer_action = self.explainer.convert_to_action()
        self.assertIsInstance(explainer_action, ExplainerAction)
        self.assertEqual(explainer_action.action()["instruction"], "Read this carefully!")
