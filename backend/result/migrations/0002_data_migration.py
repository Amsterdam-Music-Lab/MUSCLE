import logging
from tqdm import tqdm

from django.db import migrations

logger = logging.getLogger(__name__)


def populate_results(apps, schema_editor):
    ExperimentResult = apps.get_model('experiment', 'Result')
    Profile = apps.get_model('experiment', 'Profile')
    Result = apps.get_model('result', 'Result')
    for result in tqdm(ExperimentResult.objects.all()):
        session = result.session
        participant = session.participant
        new_participant = get_or_create_participant(participant, apps)
        new_session = get_or_create_session(session, new_participant, apps)
        new_result = Result.objects.create(
            session=new_session,
            created_at=result.created_at,
            question_key='',
            expected_response=result.expected_response,
            given_response=result.given_response,
            comment=result.comment,
            score=result.score,
            scoring_rule='',
            json_data=result.json_data
        )
        attempt_set_section(new_result, result)
        new_result.save()
        result.delete()
    for profile in Profile.objects.all():
        new_participant = get_or_create_participant(profile.participant, apps)
        result = Result.objects.create(
            participant=new_participant,
            question_key=profile.question,
            created_at=profile.created_at,
            given_response=profile.answer,
            score=profile.score
        )
        result.save()
    # delete former sessions and participants = will cascade down to results and profiles
    OldSession = apps.get_model('experiment', 'Session')
    OldSession.objects.all().delete()
    OldParticipant = apps.get_model('experiment', 'Participant')
    OldParticipant.objects.all().delete()


def backwards_populate_results(apps, schema_editor):
    ExperimentResult = apps.get_model('experiment', 'Result')
    Profile = apps.get_model('experiment', 'Profile')
    Result = apps.get_model('result', 'Result')
    for result in tqdm(Result.objects.all()):
        session = result.session
        if session:
            participant = session.participant
            new_participant = get_or_create_participant(participant, apps, 'experiment')
            new_session = get_or_create_session(session, new_participant, apps, 'experiment')
            new_result = ExperimentResult.objects.create(
                session=new_session,
                created_at=result.created_at,
                expected_response=result.expected_response or '',
                given_response=result.given_response or '',
                comment=result.comment,
                score=result.score,
                json_data=result.json_data
            )
            attempt_set_section(new_result, result)
            new_result.save()
        participant = result.participant
        if participant:
            new_participant = get_or_create_participant(participant, apps, 'experiment')
            profile = Profile.objects.create(
                participant=new_participant,
                created_at=result.created_at,
                question=result.question_key,
                answer=result.given_response or '',
                score=result.score
            )
            profile.save()
    # delete former sessions and participants = will cascade down to results
    OldSession = apps.get_model('session', 'Session')
    OldSession.objects.all().delete()
    OldParticipant = apps.get_model('participant', 'Participant')
    OldParticipant.objects.all().delete()


def attempt_set_section(new_result, result):
    try:
        new_result.section = result.section
    except:
        logging.warning('result {} could not set section {}'.format(new_result.id, result.section.id))


def get_or_create_participant(participant, apps, app_name='participant'):
    Participant = apps.get_model(app_name, 'Participant')
    try:
        new_participant = Participant.objects.get(
            unique_hash=participant.unique_hash
        )
    except Participant.DoesNotExist:
        new_participant = Participant.objects.create(
            unique_hash=participant.unique_hash,
            country_code=participant.country_code,
            access_info=participant.access_info
        )
        new_participant.save()
    return new_participant


def get_or_create_session(session, new_participant, apps, app_name='session'):
    Session = apps.get_model(app_name, 'Session')
    try:
        new_session = Session.objects.get(
            experiment=session.experiment,
            participant=new_participant,
            started_at=session.started_at
        )
    except Session.DoesNotExist:
        new_session = Session.objects.create(
            experiment=session.experiment,
            participant=new_participant,
            # playlist=session.playlist,
            started_at=session.started_at,
            finished_at=session.finished_at,
            json_data=session.json_data,
            final_score=session.final_score
        )
        new_session.save()
    return new_session


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0001_initial'),
        ('experiment', '0013_change_playlist_reference'),
    ]

    operations = [
        migrations.RunPython(populate_results, backwards_populate_results)
    ]
