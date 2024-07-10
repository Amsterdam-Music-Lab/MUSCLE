from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from image.models import Image
from experiment.serializers import (
    serialize_block,
    serialize_phase
)
from experiment.models import (
    Block,
    ExperimentCollection,
    Phase,
    GroupedBlock,
    SocialMediaConfig,
)
from experiment.rules.hooked import Hooked
from participant.models import Participant
from session.models import Session
from theme.models import ThemeConfig, FooterConfig, HeaderConfig


class TestExperimentCollectionViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        theme_config = create_theme_config()
        collection = ExperimentCollection.objects.create(
            name='Test Series',
            slug='test_series',
            theme_config=theme_config,
        )
        collection.social_media_config = create_social_media_config(collection)
        introductory_phase = Phase.objects.create(
            name='introduction',
            series=collection,
            index=1
        )
        cls.block1 = Block.objects.create(
            name='block1', slug='block1')
        GroupedBlock.objects.create(
            block=cls.block1,
            phase=introductory_phase
        )
        intermediate_phase = Phase.objects.create(
            name='intermediate',
            series=collection,
            index=2
        )
        cls.block2 = Block.objects.create(
            name='block2', slug='block2', theme_config=theme_config)
        cls.block3 = Block.objects.create(
            name='block3', slug='block3')
        GroupedBlock.objects.create(
            block=cls.block2,
            phase=intermediate_phase
        )
        GroupedBlock.objects.create(
            block=cls.block3,
            phase=intermediate_phase
        )
        final_phase = Phase.objects.create(
            name='final',
            series=collection,
            index=3
        )
        cls.block4 = Block.objects.create(
            name='block4', slug='block4')
        GroupedBlock.objects.create(
            block=cls.block4,
            phase=final_phase
        )

    def test_get_experiment_collection(self):
        # save participant data to request session
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        # check that first_experiments is returned correctly
        response = self.client.get('/experiment/test_series/')
        self.assertEqual(response.json().get(
            'nextBlock').get('slug'), 'block1')
        # create session
        Session.objects.create(
            block=self.block1,
            participant=self.participant,
            finished_at=timezone.now()
        )
        response = self.client.get('/experiment/test_series/')
        self.assertIn(response.json().get('nextBlock').get(
            'slug'), ('block2', 'block3'))
        self.assertEqual(response.json().get('dashboard'), [])
        Session.objects.create(
            block=self.block2,
            participant=self.participant,
            finished_at=timezone.now()
        )
        Session.objects.create(
            block=self.block3,
            participant=self.participant,
            finished_at=timezone.now()
        )
        response = self.client.get('/experiment/test_series/')
        response_json = response.json()
        self.assertEqual(response_json.get(
            'nextBlock').get('slug'), 'block4')
        self.assertEqual(response_json.get('dashboard'), [])
        self.assertEqual(response_json.get('theme').get('name'), 'test_theme')
        self.assertEqual(len(response_json['theme']['header']['score']), 3)
        self.assertEqual(response_json.get('theme').get('footer').get(
            'disclaimer'), '<p>Test Disclaimer</p>')
        self.assertEqual(response_json.get('socialMedia').get('url'), 'https://www.example.com')
        self.assertEqual(response_json.get('socialMedia').get('content'), 'Test Content')
        self.assertEqual(response_json.get('socialMedia').get('tags'), ['aml', 'toontjehoger'])
        self.assertEqual(response_json.get('socialMedia').get('channels'), ['facebook', 'twitter', 'weibo'])

    def test_get_experiment_collection_not_found(self):
        # if ExperimentCollection does not exist, return 404
        response = self.client.get('/experiment/not_found/')
        self.assertEqual(response.status_code, 404)

    def test_get_experiment_collection_inactive(self):
        # if ExperimentCollection is inactive, return 404
        collection = ExperimentCollection.objects.get(slug='test_series')
        collection.active = False
        collection.save()
        response = self.client.get('/experiment/test_series/')
        self.assertEqual(response.status_code, 404)

    def test_get_experiment_without_social_media(self):
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        Session.objects.create(
            block=self.block1,
            participant=self.participant,
            finished_at=timezone.now()
        )
        intermediate_phase = Phase.objects.get(
            name='intermediate'
        )
        intermediate_phase.dashboard = True
        intermediate_phase.save()

        ExperimentCollection.objects.create(
            name='No Social Media',
            slug='no_social_media',
            theme_config=create_theme_config(name='no_social_media')
        )

        response = self.client.get('/experiment/collection/no_social_media/')

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('socialMedia', response.json())

    def test_experiment_collection_with_dashboard(self):
        # if ExperimentCollection has dashboard set True, return list of random blocks
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        Session.objects.create(
            block=self.block1,
            participant=self.participant,
            finished_at=timezone.now()
        )
        intermediate_phase = Phase.objects.get(
            name='intermediate'
        )
        intermediate_phase.dashboard = True
        intermediate_phase.save()
        # check that first_experiments is returned correctly
        response = self.client.get('/experiment/test_series/')
        self.assertEqual(type(response.json().get('dashboard')), list)

    def test_experiment_collection_total_score(self):
        """ Test calculation of total score for grouped block on dashboard """
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        Session.objects.create(
            block=self.block2,
            participant=self.participant,
            finished_at=timezone.now(),
            final_score=8
        )
        intermediate_phase = Phase.objects.get(
            name='intermediate'
        )
        intermediate_phase.dashboard = True
        intermediate_phase.save()
        serialized_coll_1 = serialize_phase(intermediate_phase, self.participant)
        total_score_1 = serialized_coll_1['totalScore']
        self.assertEqual(total_score_1, 8)
        Session.objects.create(
            block=self.block3,
            participant=self.participant,
            finished_at=timezone.now(),
            final_score=8
        )
        serialized_coll_2 = serialize_phase(intermediate_phase, self.participant)
        total_score_2 = serialized_coll_2['totalScore']
        self.assertEqual(total_score_2, 16)


class ExperimentViewsTest(TestCase):

    def test_serialize_block(self):
        # Create an block
        block = Block.objects.create(
            slug='test-block',
            name='Test Block',
            description='This is a test block',
            image=Image.objects.create(
                title='Test',
                description='',
                file='test-image.jpg',
                alt='Test',
                href='https://www.example.com',
                rel='',
                target='_self',
            ),
            theme_config=create_theme_config()
        )
        participant = Participant.objects.create()
        Session.objects.bulk_create([
            Session(block=block, participant=participant, finished_at=timezone.now()) for index in range(3)
        ])

        # Call the serialize_block function
        serialized_block = serialize_block(block, participant)

        # Assert the serialized data
        self.assertEqual(
            serialized_block['slug'], 'test-block'
        )
        self.assertEqual(
            serialized_block['name'], 'Test Block'
        )
        self.assertEqual(
            serialized_block['description'], 'This is a test block'
        )
        self.assertEqual(
            serialized_block['image'], {
                'title': 'Test',
                'description': '',
                'file': f'{settings.BASE_URL}/upload/test-image.jpg',
                'href': 'https://www.example.com',
                'alt': 'Test',
                'rel': '',
                'target': '_self',
                'tags': []
            }
        )

    def test_get_block(self):
        # Create an block
        block = Block.objects.create(
            slug='test-block',
            name='Test Block',
            description='This is a test block',
            image=Image.objects.create(
                file='test-image.jpg'
            ),
            rules=Hooked.ID,
            theme_config=create_theme_config(),
            rounds=3,
            bonus_points=42,
        )
        participant = Participant.objects.create()
        Session.objects.bulk_create([
            Session(block=block, participant=participant, finished_at=timezone.now()) for index in range(3)
        ])

        response = self.client.get('/experiment/block/test-block/')

        self.assertEqual(
            response.json()['slug'], 'test-block'
        )
        self.assertEqual(
            response.json()['name'], 'Test Block'
        )
        self.assertEqual(
            response.json()['theme']['name'], 'test_theme'
        )
        self.assertEqual(
            len(response.json()['theme']['header']['score']), 3
        )
        self.assertEqual(
            response.json()['theme']['footer']['disclaimer'], '<p>Test Disclaimer</p>'
        )
        self.assertEqual(
            response.json()['rounds'], 3
        )
        self.assertEqual(
            response.json()['bonus_points'], 42
        )


def create_theme_config(name='test_theme') -> ThemeConfig:
    theme_config = ThemeConfig.objects.create(
            name=name,
            description='Test Theme',
            heading_font_url='https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Micro+5&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap',
            body_font_url='https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Micro+5&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap',
            logo_image=Image.objects.create(file='test-logo.jpg'),
            background_image=Image.objects.create(file='test-background.jpg'),
    )
    HeaderConfig.objects.create(
        theme=theme_config,
        show_score=True
    )
    footer_config = FooterConfig.objects.create(
        theme=theme_config,
        disclaimer='Test Disclaimer',
        privacy='Test Privacy',
    )
    footer_config.logos.add(Image.objects.create(file='test-logo.jpg'))

    return theme_config


def create_social_media_config(
        collection: ExperimentCollection) -> SocialMediaConfig:
    return SocialMediaConfig.objects.create(
        experiment_collection=collection,
        url='https://www.example.com',
        content='Test Content',
        channels=['facebook', 'twitter', 'weibo'],
        tags=['aml', 'toontjehoger']
    )
