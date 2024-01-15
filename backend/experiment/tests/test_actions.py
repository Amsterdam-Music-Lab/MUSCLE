from django.test import TestCase

from experiment.actions.utils import randomize_playhead


class TestActions(TestCase):

    def test_randomize_playhead(self):
        silence_time = 4
        min_jitter = 5
        max_jitter = 10
        unjittered_playhead = randomize_playhead(min_jitter, max_jitter, silence_time, True)
        assert unjittered_playhead == silence_time
        jittered_playhead = randomize_playhead(min_jitter, max_jitter, silence_time, False)
        assert jittered_playhead >= silence_time + min_jitter
