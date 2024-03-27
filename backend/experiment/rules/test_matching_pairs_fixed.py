from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist, Section
from session.models import Session
from experiment.rules.matching_pairs_fixed import MatchingPairsFixed


class MatchingPairsFixedTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.experiment = Experiment.objects.create(
            name='Test Experiment',
            slug='test-experiment',
            rules='matching_pairs_lite'
        )
        self.playlist = Playlist.objects.create(
            name='Test Playlist'
        )

    def test_select_sections_original_degraded(self):

        self.section1 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Original'
        )
        self.section2 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Degradation'
        )
        self.section3 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Original'
        )
        self.section4 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Degradation'
        )
        self.section5 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Original'
        )
        self.section6 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Degradation'
        )
        self.section7 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Original'
        )
        self.section8 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Degradation'
        )
        self.participant = Participant.objects.create(
            unique_hash='testhash'
        )
        self.session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist,
        )

        rule = MatchingPairsFixed()
        sections = rule.select_sections(self.session)
        deterministic_order = [6, 5, 1, 4, 7, 8, 2, 3]

        self.assertEqual(len(sections), 8)
        self.assertIn(self.section1, sections)
        self.assertIn(self.section2, sections)
        self.assertIn(self.section3, sections)
        self.assertIn(self.section4, sections)
        self.assertIn(self.section5, sections)
        self.assertIn(self.section6, sections)
        self.assertIn(self.section7, sections)
        self.assertIn(self.section8, sections)
        self.assertEqual(sections.count(self.section1), 1)
        self.assertEqual(sections.count(self.section2), 1)
        self.assertEqual(sections.count(self.section3), 1)
        self.assertEqual(sections.count(self.section4), 1)
        self.assertEqual(sections.count(self.section5), 1)
        self.assertEqual(sections.count(self.section6), 1)
        self.assertEqual(sections.count(self.section7), 1)
        self.assertEqual(sections.count(self.section8), 1)

        for i in range(8):
            self.assertEqual(sections[i].pk, deterministic_order[i])

    def test_select_sections_original_original(self):

        self.section1 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Original'
        )
        self.section2 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Original'
        )
        self.section3 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Original'
        )
        self.section4 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Original'
        )
        self.section5 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Original'
        )
        self.section6 = Section.objects.create(
            playlist=self.playlist,
            group='Group 1',
            tag='Original'
        )
        self.section7 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Original'
        )
        self.section8 = Section.objects.create(
            playlist=self.playlist,
            group='Group 2',
            tag='Original'
        )
        self.participant = Participant.objects.create(
            unique_hash='testhash'
        )
        self.session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist,
        )

        rule = MatchingPairsFixed()
        sections = rule.select_sections(self.session)
        deterministic_order = [9, 10, 13, 12, 14, 13, 15, 11, 10, 14, 16, 15, 16, 11, 9, 12]

        self.assertEqual(len(sections), 16)
        self.assertIn(self.section1, sections)
        self.assertIn(self.section2, sections)
        self.assertIn(self.section3, sections)
        self.assertIn(self.section4, sections)
        self.assertIn(self.section5, sections)
        self.assertIn(self.section6, sections)
        self.assertIn(self.section7, sections)
        self.assertIn(self.section8, sections)
        self.assertEqual(sections.count(self.section1), 2)
        self.assertEqual(sections.count(self.section2), 2)
        self.assertEqual(sections.count(self.section3), 2)
        self.assertEqual(sections.count(self.section4), 2)
        self.assertEqual(sections.count(self.section5), 2)
        self.assertEqual(sections.count(self.section6), 2)
        self.assertEqual(sections.count(self.section7), 2)
        self.assertEqual(sections.count(self.section8), 2)

        for i in range(8):
            self.assertEqual(sections[i].pk, deterministic_order[i])
