from django.apps import apps
from django.test import TestCase
from django.db.migrations.executor import MigrationExecutor
from django.db import connection
from unittest import skip


class TestMigrations(TestCase):

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.migrate_from and self.migrate_to, \
            "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class TagsTestCase(TestMigrations):

    migrate_from = '0001_initial'
    migrate_to = '0002_data_migration'

    def setUpBeforeMigration(self, apps):
        OldSession = apps.get_model('experiment', 'Session')
        Section = apps.get_model('section', 'Section')
        OldParticipant = apps.get_model('experiment', 'Participant')
        Playlist = apps.get_model('section', 'Playlist')
        OldResult = apps.get_model('experiment', 'Result')
        Profile = apps.get_model('experiment', 'Profile')
        Experiment = apps.get_model('experiment', 'Experiment')
        self.playlist = Playlist.objects.create(
            name='Testing'
        )
        self.sections = [
            Section.objects.create(
                playlist=self.playlist,
                artist='Superstar',
                name='Great track',
                filename='/Some/path'
            ),
            Section.objects.create(
                playlist=self.playlist,
                artist='Even bigger star',
                name='Even greater track',
                filename='/Another/path'
            )
        ]
        self.participant = OldParticipant.objects.create(
            unique_hash=42,
            country_code='nl',
            access_info='some browser and OS'
        )
        self.experiment = Experiment.objects.create(
            name='TestExperiment',
            slug='tst'
        )
        self.experiment.playlists.add(self.playlist)
        self.experiment.save()
        self.session = OldSession.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )
        self.result = OldResult.objects.create(
            session=self.session,
            section=self.sections[0],
            comment='Weird comment'
        )
        self.profile = Profile.objects.create(
            participant=self.participant,
            question='some_question'
        )

    # def test_playlist_migrated(self):
    #     Playlist = self.apps.get_model('section', 'Playlist')
    #     Section = self.apps.get_model('section', 'Section')
    #     playlists = Playlist.objects.filter(name=self.playlist.name)
    #     sections = Section.objects.all()
    #     assert playlists.count() == 1
    #     assert sections.count() == len(self.sections)
    #     assert sections.first().playlist.name == self.playlist.name

    def test_participant_migrated(self):
        Participant = self.apps.get_model('participant', 'Participant')
        participant = Participant.objects.first()
        assert participant.unique_hash == self.participant.unique_hash
    
    @skip  
    def test_session_migrated(self):
        Session = self.apps.get_model('session', 'Session')
        session = Session.objects.first()
        assert session.experiment.slug == self.session.experiment.slug
        assert session.participant.unique_hash == self.participant.unique_hash

    def test_result_migrated(self):
        Result = self.apps.get_model('result', 'Result')
        result = Result.objects.filter(session__isnull=False).first()
        assert result.session.started_at == self.session.started_at
        assert result.section.name == self.sections[0].name
        assert result.comment == 'Weird comment'
        profile = Result.objects.filter(participant_isnull=False).first()
        assert profile.participant.unique_hash == self.participant.unique_hash
        assert profile.question_key == self.profile.question
