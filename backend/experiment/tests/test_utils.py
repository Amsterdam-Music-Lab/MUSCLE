from django.test import TestCase

from experiment.utils import create_player_labels

class TestExperimentUtils(TestCase):
    
    def test_create_player_labels(self):
        labels = create_player_labels(3, 'alphabetic')
        assert labels == ['A', 'B', 'C']
        labels = create_player_labels(4, 'roman')
        assert labels == ['I', 'II', 'III', 'IV']
        labels = create_player_labels(2)
        assert labels == ['1', '2']