from django.test import TestCase
from experiment.models import Block, Phase
from section.models import Playlist
from participant.models import Participant
from session.models import Session
from experiment.rules.categorization import Categorization

class CategorizationRuleTest(TestCase):
    fixtures = ["choice_lists", "demographics", "categorization"]

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.get(name='Categorization')
        cls.playlist._update_sections()
        cls.participant = Participant.objects.create()
        cls.block = Block.objects.get(identifier='cat')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )
        cls.rules = cls.block.get_rules()

    def test_explainer(self):
        categorization = Categorization()
        explainer = categorization.get_intro_explainer().action()
        self.assertEqual(explainer['instruction'],
                         'This is a listening experiment in which you have to respond to short sound sequences.')
        self.assertEqual(explainer['button']['label'], 'Ok')

    def test_plan_experiment_and_phase(self):
        categorization = Categorization()

        # Test first next_round
        first_next_round = categorization.next_round(self.session)

        # Test plan experiment
        self.assertEqual(self.session.json_data.get('phase'), 'training')
        self.assertEqual(self.session.json_data.get('training_rounds'), '0')

        self.assertIn(self.session.json_data.get('group'), ['C1', 'C2', 'S1', 'S2'])
        self.assertIn(
            self.session.json_data.get('choices')[0]['color'],
            ['colorNeutral1', 'colorNeutral2'],
        )
        self.assertIn(self.session.json_data.get('choices')[0]['value'], ["A", "B"])

        if self.session.json_data.get('group') == 'C1':
            self.assertEqual(self.session.json_data.get('assigned_group'), 'Crossed direction, Pair 1')
        if self.session.json_data.get('group') == 'C2':
            self.assertEqual(self.session.json_data.get('assigned_group'), 'Crossed direction, Pair 2')
        if self.session.json_data.get('group') == 'S1':
            self.assertEqual(self.session.json_data.get('assigned_group'), 'Same direction, Pair 1')
        if self.session.json_data.get('group') == 'S2':
            self.assertEqual(self.session.json_data.get('assigned_group'), 'Same direction, Pair 2')

        ph = "___"  # placeholder
        if self.session.json_data.get('button_order') == 'neutral':
            self.assertEqual(self.session.json_data.get('button_colors'), 'Blue left, Orange right')
            if self.session.json_data.get('stimuli_a') == "BLUE":
                self.assertEqual(
                    self.session.json_data.get('choices'),
                    [{"value": "A", "label": ph}, {"value": "B", "label": ph}],
                )
            if self.session.json_data.get('stimuli_a') == "ORANGE":
                self.assertEqual(
                    self.session.json_data.get('choices'),
                    [{"value": "B", "label": ph}, {"value": "A", "label": ph}],
                )

        if self.session.json_data.get('button_order') == 'neutral-inverted':
            self.assertEqual(self.session.json_data.get('button_colors'), 'Orange left, Blue right')
            if self.session.json_data.get('stimuli_a') == "BLUE":
                self.assertEqual(
                    self.session.json_data.get('choices'),
                    [{"value": "B", "label": ph}, {"value": "A", "label": ph}],
                )
            if self.session.json_data.get('stimuli_a') == "ORANGE":
                self.assertEqual(
                    self.session.json_data.get('choices'),
                    [{"value": "A", "label": ph}, {"value": "B", "label": ph}],
                )

        # Test explainer
        self.assertEqual(categorization.get_intro_explainer().action()['instruction'], first_next_round[0].instruction)

        # Test second next_round
        second_next_round = categorization.next_round(self.session)
        self.assertEqual(self.session.json_data.get('phase'), 'training-1A')
        self.assertEqual(self.session.json_data.get('training_rounds'), '0')
        self.assertEqual(self.session.json_data.get('phase'), 'training-1A')
