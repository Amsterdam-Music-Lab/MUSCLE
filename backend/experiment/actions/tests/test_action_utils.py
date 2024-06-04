from django.test import TestCase

from experiment.actions.utils import randomize_playhead


class TestActions(TestCase):

    def test_randomize_playhead(self):
        min_jitter = 5
        max_jitter = 10
        unjittered_playhead = randomize_playhead(min_jitter, max_jitter, True)
        assert unjittered_playhead == 0
        jittered_playhead = randomize_playhead(min_jitter, max_jitter, False)
        assert jittered_playhead >= min_jitter
