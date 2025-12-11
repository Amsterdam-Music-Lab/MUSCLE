from django.test import TestCase

from experiment.models import Block, Experiment, Phase

from question.forms import QuestionListForm
from question.models import QuestionInList, QuestionList
from question.banks import PRESET_BANKS


class QuestionListFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        experiment = Experiment.objects.create(slug='test_experiment')
        phase = Phase.objects.create(experiment=experiment)
        cls.block = Block.objects.create(phase=phase, slug='test_block')

    def test_add_from_question_bank(self):
        self.assertEqual(QuestionInList.objects.count(), 0)
        form = QuestionListForm()
        ql = QuestionList.objects.create(
            name='test question list', block=self.block, index=0
        )
        form.add_questions_from_bank(ql, 'DEMOGRAPHICS')
        self.assertEqual(
            QuestionInList.objects.count(), len(PRESET_BANKS.get('DEMOGRAPHICS'))
        )
