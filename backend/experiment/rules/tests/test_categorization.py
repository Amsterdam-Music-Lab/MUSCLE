from django.test import TestCase
from experiment.models import Block, Experiment, Phase
from section.models import Playlist, Section, Song
from participant.models import Participant
from session.models import Session
from experiment.rules.categorization import Categorization
from result.models import Result

class CategorizationRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        section_csv = (
            "P1 Training A-430Hz(2.6k)-360Hz(3.1k)-290Hz(3.6k)-220Hz(4.1k)-150Hz(4.6k).wav,C0T1A,0.0,1.25,CAT/C0T1A.wav,1A,CROSSED\n"
            "P1 Training B-150Hz(4.6k)-220Hz(4.1k)-290Hz(3.6k)-360Hz(3.1k)-430Hz(2.6k).wav,C0T1B,0.0,1.25,CAT/C0T1B.wav,1B,CROSSED\n"
            "P2 Training A-405Hz(2.1k)-330Hz(2.7k)-255Hz(3.3k)-180Hz(3.9k)-105Hz(4.5k).wav,C0T2A,0.0,1.25,CAT/C0T2A.wav,2A,CROSSED\n"
            "P2 Training B-105Hz(4.5k)-180Hz(3.9k)-255Hz(3.3k)-330Hz(2.7k)-405Hz(2.1k).wav,C0T2B,0.0,1.25,CAT/C0T2B.wav,2B,CROSSED\n"
            "P1 Vocoded A-430Hz(2.6k)-360Hz(3.1k)-290Hz(3.6k)-220Hz(4.1k)-150Hz(4.6k).wav,C1VnP1A,0.0,1.25,CAT/C1VnP1A.wav,1A,CROSSED\n"
            "P1 Vocoded B-150Hz(4.6k)-220Hz(4.1k)-290Hz(3.6k)-360Hz(3.1k)-430Hz(2.6k).wav,C1VnP1B,0.0,1.25,CAT/C1VnP1B.wav,1B,CROSSED\n"
            "P2 Vocoded A-405Hz(2.1k)-330Hz(2.7k)-255Hz(3.3k)-180Hz(3.9k)-105Hz(4.5k).wav,C1VnP2A,0.0,1.25,CAT/C1VnP2A.wav,2A,CROSSED\n"
            "P2 Vocoded B-105Hz(4.5k)-180Hz(3.9k)-255Hz(3.3k)-330Hz(2.7k)-405Hz(2.1k).wav,C1VnP2B,0.0,1.25,CAT/C1VnP2B.wav,2B,CROSSED\n"
            "P1 No-Formant A-430Hz-360Hz-290Hz-220Hz-150Hz.wav,C2PnF1A,0.0,1.25,CAT/C2PnF1A.wav,1A,CROSSED\n"
            "P1 No-Formant B-150Hz-220Hz-290Hz-360Hz-430Hz.wav,C2PnF1B,0.0,1.25,CAT/C2PnF1B.wav,1B,CROSSED\n"
            "P2 No-Formant A-405Hz-330Hz-255Hz-180Hz-105Hz.wav,C2PnF2A,0.0,1.25,CAT/C2PnF2A.wav,2A,CROSSED\n"
            "P2 No-Formant B-105Hz-180Hz-255Hz-330Hz-405Hz.wav,C2PnF2B,0.0,1.25,CAT/C2PnF2B.wav,2B,CROSSED\n"
            "P1 F0=290Hz A-290Hz(2.6k-3.1k-3.6k-4.1k-4.6k).wav,C3FcP1A,0.0,1.25,CAT/C3FcP1A.wav,1A,CROSSED\n"
            "P1 F0=290Hz B-290Hz(4.6k-4.1k-3.6k-3.1k-2.6k).wav,C3FcP1B,0.0,1.25,CAT/C3FcP1B.wav,1B,CROSSED\n"
            "P2 F0=255Hz A-255Hz(2.1k-2.7k-3.3k-3.9k-4.5k).wav,C3FcP2A,0.0,1.25,CAT/C3FcP2A.wav,2A,CROSSED\n"
            "P2 F0=255Hz B-255Hz(4.5k-3.9k-3.3k-2.7k-2.1k).wav,C3FcP2B,0.0,1.25,CAT/C3FcP2B.wav,2B,CROSSED\n"
            "P1 Formant3.6k A-430Hz(3.6k)-360Hz(3.6k)-290Hz(3.6k)-220Hz(3.6k)-150Hz(3.6k).wav,C4PcF1A,0.0,1.25,CAT/C4PcF1A.wav,1A,CROSSED\n"
            "P1 Formant3.6k B-150Hz(3.6k)-220Hz(3.6k)-290Hz(3.6k)-360Hz(3.6k)-430Hz(3.6k).wav,C4PcF1B,0.0,1.25,CAT/C4PcF1B.wav,1B,CROSSED\n"
            "P2 Formant3.3k A-405Hz(3.3k)-330Hz(3.3k)-255Hz(3.3k)-180Hz(3.3k)-105Hz(3.3k).wav,C4PcF2A,0.0,1.25,CAT/C4PcF2A.wav,2A,CROSSED\n"
            "P2 Formant3.3k B-105Hz(3.3k)-180Hz(3.3k)-255Hz(3.3k)-330Hz(3.3k)-405Hz(3.3k).wav,C4PcF2B,0.0,1.25,CAT/C4PcF2B.wav,2B,CROSSED\n"
            "P1 Formants = Pitches A-150Hz(2.6k)-220Hz(3.1k)-290Hz(3.6k)-360Hz(4.1k)-430Hz(4.6k).wav,C5P=F1A,0.0,1.25,CAT/C5P=F1A.wav,1A,CROSSED\n"
            "P1 Formants = Pitches B-430Hz(4.6k)-360Hz(4.1k)-290Hz(3.6k)-220Hz(3.1k)-150Hz(2.6k).wav,C5P=F1B,0.0,1.25,CAT/C5P=F1B.wav,1B,CROSSED\n"
            "P2 Formants = Pitches A-105Hz(2.1k)-180Hz(2.7k)-255Hz(3.3k)-330Hz(3.9k)-405Hz(4.5k).wav,C5P=F2A,0.0,1.25,CAT/C5P=F2A.wav,2A,CROSSED\n"
            "P2 Formants = Pitches B-405Hz(4.5k)-330Hz(3.9k)-255Hz(3.3k)-180Hz(2.7k)-105Hz(2.1k).wav,C5P=F2B,0.0,1.25,CAT/C5P=F2B.wav,2B,CROSSED\n"
            "P1 Training A-150Hz(2.6k)-220Hz(3.1k)-290Hz(3.6k)-360Hz(4.1k)-430Hz(4.6k).wav,S0T1A,0.0,1.25,CAT/S0T1A.wav,1A,SAME\n"
            "P1 Training B-430Hz(4.6k)-360Hz(4.1k)-290Hz(3.6k)-220Hz(3.1k)-150Hz(2.6k).wav,S0T1B,0.0,1.25,CAT/S0T1B.wav,1B,SAME\n"
            "P2 Training A-105Hz(2.1k)-180Hz(2.7k)-255Hz(3.3k)-330Hz(3.9k)-405Hz(4.5k).wav,S0T2A,0.0,1.25,CAT/S0T2A.wav,2A,SAME\n"
            "P2 Training B-405Hz(4.5k)-330Hz(3.9k)-255Hz(3.3k)-180Hz(2.7k)-105Hz(2.1k).wav,S0T2B,0.0,1.25,CAT/S0T2B.wav,2B,SAME\n"
            "P1 Vocoded A-150Hz(2.6k)-220Hz(3.1k)-290Hz(3.6k)-360Hz(4.1k)-430Hz(4.6k).wav,S1VnP1A,0.0,1.25,CAT/S1VnP1A.wav,1A,SAME\n"
            "P1 Vocoded B-430Hz(4.6k)-360Hz(4.1k)-290Hz(3.6k)-220Hz(3.1k)-150Hz(2.6k).wav,S1VnP1B,0.0,1.25,CAT/S1VnP1B.wav,1B,SAME\n"
            "P2 Vocoded A-105Hz(2.1k)-180Hz(2.7k)-255Hz(3.3k)-330Hz(3.9k)-405Hz(4.5k).wav,S1VnP2A,0.0,1.25,CAT/S1VnP2A.wav,2A,SAME\n"
            "P2 Vocoded B-405Hz(4.5k)-330Hz(3.9k)-255Hz(3.3k)-180Hz(2.7k)-105Hz(2.1k).wav,S1VnP2B,0.0,1.25,CAT/S1VnP2B.wav,2B,SAME\n"
            "P1 No-Formant A-150Hz-220Hz-290Hz-360Hz-430Hz.wav,S2PnF1A,0.0,1.25,CAT/S2PnF1A.wav,1A,SAME\n"
            "P1 No-Formant B-430Hz-360Hz-290Hz-220Hz-150Hz.wav,S2PnF1B,0.0,1.25,CAT/S2PnF1B.wav,1B,SAME\n"
            "P2 No-Formant A-105Hz-180Hz-255Hz-330Hz-405Hz.wav,S2PnF2A,0.0,1.25,CAT/S2PnF2A.wav,2A,SAME\n"
            "P2 No-Formant B-405Hz-330Hz-255Hz-180Hz-105Hz.wav,S2PnF2B,0.0,1.25,CAT/S2PnF2B.wav,2B,SAME\n"
            "P1 F0=290Hz A-290Hz(2.6k-3.1k-3.6k-4.1k-4.6k).wav,S3FcP1A,0.0,1.25,CAT/S3FcP1A.wav,1A,SAME\n"
            "P1 F0=290Hz B-290Hz(4.6k-4.1k-3.6k-3.1k-2.6k).wav,S3FcP1B,0.0,1.25,CAT/S3FcP1B.wav,1B,SAME\n"
            "P2 F0=255Hz A-255Hz(2.1k-2.7k-3.3k-3.9k-4.5k).wav,S3FcP2A,0.0,1.25,CAT/S3FcP2A.wav,2A,SAME\n"
            "P2 F0=255Hz B-255Hz(4.5k-3.9k-3.3k-2.7k-2.1k).wav,S3FcP2B,0.0,1.25,CAT/S3FcP2B.wav,2B,SAME\n"
            "P1 Formant3.6k A-150Hz(3.6k)-220Hz(3.6k)-290Hz(3.6k)-360Hz(3.6k)-430Hz(3.6k).wav,S4PcF1A,0.0,1.25,CAT/S4PcF1A.wav,1A,SAME\n"
            "P1 Formant3.6k B-430Hz(3.6k)-360Hz(3.6k)-290Hz(3.6k)-220Hz(3.6k)-150Hz(3.6k).wav,S4PcF1B,0.0,1.25,CAT/S4PcF1B.wav,1B,SAME\n"
            "P2 Formant3.3k A-105Hz(3.3k)-180Hz(3.3k)-255Hz(3.3k)-330Hz(3.3k)-405Hz(3.3k).wav,S4PcF2A,0.0,1.25,CAT/S4PcF2A.wav,2A,SAME\n"
            "P2 Formant3.3k B-405Hz(3.3k)-330Hz(3.3k)-255Hz(3.3k)-180Hz(3.3k)-105Hz(3.3k).wav,S4PcF2B,0.0,1.25,CAT/S4PcF2B.wav,2B,SAME\n"
            "P1 Formants x Pitches A-430Hz(2.6k)-360Hz(3.1k)-290Hz(3.6k)-220Hz(4.1k)-150Hz(4.6k).wav,S5PxF1A,0.0,1.25,CAT/S5PxF1A.wav,1A,SAME\n"
            "P1 Formants x Pitches B-150Hz(4.6k)-220Hz(4.1k)-290Hz(3.6k)-360Hz(3.1k)-430Hz(2.6k).wav,S5PxF1B,0.0,1.25,CAT/S5PxF1B.wav,1B,SAME\n"
            "P2 Formants x Pitches A-405Hz(2.1k)-330Hz(2.7k)-255Hz(3.3k)-180Hz(3.9k)-105Hz(4.5k).wav,S5PxF2A,0.0,1.25,CAT/S5PxF2A.wav,2A,SAME\n"
            "P2 Formants x Pitches B-105Hz(4.5k)-180Hz(3.9k)-255Hz(3.3k)-330Hz(2.7k)-405Hz(2.1k).wav,S5PxF2B,0.0,1.25,CAT/S5PxF2B.wav,2B,SAME\n"
        )
        cls.playlist = Playlist.objects.create(name='TestCategorization')
        cls.playlist.csv = section_csv
        cls.playlist._update_sections()
        cls.participant = Participant.objects.create()
        cls.block = Block.objects.create(rules='CATEGORIZATION', slug='cat')
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
        self.assertEqual(explainer['button_label'], 'Ok')

    def test_plan_experiment_and_phase(self):
        categorization = Categorization()

        # Test first next_round
        first_next_round = categorization.next_round(self.session)

        # Test plan experiment
        self.assertEqual(self.session.json_data.get('phase'), 'training')
        self.assertEqual(self.session.json_data.get('training_rounds'), '0')

        self.assertIn(self.session.json_data.get('group'), ['C1', 'C2', 'S1', 'S2'])
        self.assertIn(self.session.json_data.get('button_order'), ['neutral', 'neutral-inverted'])
        self.assertIn(self.session.json_data.get('stimuli_a'), ['BLUE', 'ORANGE'])

        if self.session.json_data.get('stimuli_a') == "BLUE":
            self.assertEqual(self.session.json_data.get('pair_colors'), "A = Blue, B = Orange")
        if self.session.json_data.get('stimuli_a') == "ORANGE":
            self.assertEqual(self.session.json_data.get('pair_colors'), "A = Orange, B = Blue")

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
                self.assertEqual(self.session.json_data.get('choices'), {"A": ph, "B": ph})
            if self.session.json_data.get('stimuli_a') == "ORANGE":
                self.assertEqual(self.session.json_data.get('choices'), {"B": ph, "A": ph})

        if self.session.json_data.get('button_order') == 'neutral-inverted':
            self.assertEqual(self.session.json_data.get('button_colors'), 'Orange left, Blue right')
            if self.session.json_data.get('stimuli_a') == "BLUE":
                self.assertEqual(self.session.json_data.get('choices'), {"B": ph, "A": ph})
            if self.session.json_data.get('stimuli_a') == "ORANGE":
                self.assertEqual(self.session.json_data.get('choices'), {"A": ph, "B": ph})

        # Test explainer
        self.assertEqual(categorization.get_intro_explainer().action()['instruction'], first_next_round[0].instruction)

        #Test second next_round
        second_next_round = categorization.next_round(self.session)
        self.assertEqual(self.session.json_data.get('phase'), 'training-1A')
        self.assertEqual(self.session.json_data.get('training_rounds'), '0')
        self.assertEqual(self.session.json_data.get('phase'), 'training-1A')

        # Test section sequence training phase
        if self.session.json_data.get('group') == 'C1':
            sections = Section.objects.filter(group="CROSSED", tag__contains="1", song__artist__contains="Training")
            for section in sections:
                        self.assertIn(section.id, self.session.json_data.get('sequence'))
        if self.session.json_data.get('group') == 'C2':
            sections = Section.objects.filter(group="CROSSED", tag__contains="2", song__artist__contains="Training")
            for section in sections:
                        self.assertIn(section.id, self.session.json_data.get('sequence'))

        if self.session.json_data.get('group') == 'S1':
            sections = Section.objects.filter(group="SAME", tag__contains="1", song__artist__contains="Training")
            for section in sections:
                        self.assertIn(section.id, self.session.json_data.get('sequence'))
        if self.session.json_data.get('group') == 'S2':
            sections = Section.objects.filter(group="SAME", tag__contains="2", song__artist__contains="Training")
            for section in sections:
                        self.assertIn(section.id, self.session.json_data.get('sequence'))
