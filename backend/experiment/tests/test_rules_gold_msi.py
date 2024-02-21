from django.test import TestCase
from experiment.rules.gold_msi import GoldMSI


class TestGoldMSI(TestCase):
    def test_init(self):
        goldMSI = GoldMSI()
        assert goldMSI.ID == 'GOLD_MSI'
        
    def test_first_round(self):
        goldMSI = GoldMSI()
        result = goldMSI.first_round()

        assert result[0].__class__.__name__ == 'Consent'
        assert result[0].ID == 'CONSENT'

