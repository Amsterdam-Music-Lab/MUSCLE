from django.test import TestCase

from experiment.models import Block, Experiment, Phase

from question.forms import QuestionSeriesForm
from question.models import QuestionInSeries, QuestionSeries
from question.preset_catalogues import PRESET_CATALOGUES

class QuestionSeriesFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        experiment = Experiment.objects.create(slug='test_experiment')
        phase = Phase.objects.create(experiment=experiment)
        cls.block = Block.objects.create(phase=phase, slug='test_block')

    def test_add_from_predefined_catalogue(self):
        self.assertEqual(QuestionInSeries.objects.count(), 0)
        form = QuestionSeriesForm()
        series = QuestionSeries.objects.create(name='test series', block=self.block, index=0)
        form.add_questions_from_catalogue(series, 'DEMOGRAPHICS')
        self.assertEqual(QuestionInSeries.objects.count(), len(PRESET_CATALOGUES.get('DEMOGRAPHICS')))
