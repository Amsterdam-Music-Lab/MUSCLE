from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from experiment.models import Experiment
from experiment.rules.gold_msi import GoldMSI


class TestGoldMSI(TestCase):
    @classmethod
    def setUpTestData(cls):       
        Experiment.objects.create(
            name='test_md',
            slug='MARKDOWN',
            consent=SimpleUploadedFile('consent.md', b'#test', content_type='text/html')
        )
        
    def test_init(self):
        goldMSI = GoldMSI()
        assert goldMSI.ID == 'GOLD_MSI'
        
    def test_first_round(self):
        experiment = Experiment.objects.first()
        goldMSI = GoldMSI()
        result = goldMSI.first_round(experiment)

        assert result[0].__class__.__name__ == 'Consent'
        assert result[0].ID == 'CONSENT'

