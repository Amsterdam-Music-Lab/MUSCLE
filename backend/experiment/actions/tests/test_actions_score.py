import unittest
from unittest.mock import Mock

from experiment.actions.score import Score


class TestScore(unittest.TestCase):

    def setUp(self):
        self.mock_session = Mock()
        self.mock_session.last_score.return_value = 10
        self.mock_session.last_song.return_value = "Test Song"
        self.mock_session.total_score.return_value = 50
        self.mock_session.get_rounds_passed.return_value = 2
        self.mock_session.block.rounds = 5

    def test_initialization_full_parameters(self):
        score = Score(
            session=self.mock_session,
            title="Test Title",
            score=100,
            score_message="Score is 100",
            config={'show_section': True, 'show_total_score': True},
            icon="icon-test",
            timer=5,
            feedback="Test Feedback",
        )
        self.assertEqual(score.title, "Test Title")
        self.assertEqual(score.score, 100)
        self.assertEqual(score.score_message, "Score is 100")
        self.assertEqual(score.feedback, "Test Feedback")
        self.assertEqual(
            score.config, {'show_section': True, 'show_total_score': True})
        self.assertEqual(score.icon, "icon-test")
        self.assertEqual(score.texts, {
            'score': 'Total Score',
            'next': 'Next',
            'listen_explainer': 'You listened to:'
        })
        self.assertEqual(score.timer, 5)

    def test_initialization_minimal_parameters(self):
        score = Score(session=self.mock_session)
        self.assertIn('Round', score.title)
        self.assertEqual(score.score, 10)
        self.assertEqual(score.score_message, score.default_score_message(score.score))
        self.assertIsNone(score.feedback)
        self.assertEqual(
            score.config, {'show_section': False, 'show_total_score': False})
        self.assertIsNone(score.icon)
        self.assertEqual(score.texts, {
            'score': 'Total Score',
            'next': 'Next',
            'listen_explainer': 'You listened to:'
        })
        self.assertIsNone(score.timer)

    def test_action_serialization(self):
        score = Score(session=self.mock_session, config={
                      'show_section': True, 'show_total_score': True})
        action = score.action()
        self.assertIn('view', action)
        self.assertIn('last_song', action)
        self.assertIn('total_score', action)
        self.assertIn('score', action)
        self.assertIn('score_message', action)
        self.assertIn('texts', action)
        self.assertIn('feedback', action)
        self.assertIn('icon', action)
        self.assertIn('timer', action)

    def test_default_score_message(self):
        score = Score(session=self.mock_session)
        self.assertIn(score.default_score_message(10), ["Correct"])  # Positive
        self.assertIn(score.default_score_message(0), ["No points"])  # Zero
        self.assertIn(score.default_score_message(-5),
                      ["Incorrect"])  # Negative
        self.assertIn(score.default_score_message(None), ["No points"])  # None


if __name__ == '__main__':
    unittest.main()
