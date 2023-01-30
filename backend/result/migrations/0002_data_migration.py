from django.db import migrations

def populate_results(apps, schema_editor):
    ExperimentResult = apps.get_model('experiment', 'Result')
    Result = apps.get_model('result', 'Result')
    for result in ExperimentResult.objects.all():
        section = result.section
        if section:
            playlist = result.section.playlist
            new_playlist = get_or_create_playlist(playlist, apps)
            new_section = get_or_create_section(section, new_playlist, apps)
        else:
            new_section = None
        session = result.session
        participant = session.participant
        new_participant = get_or_create_participant(participant, apps)
        new_session = get_or_create_session(session, new_participant, apps)
        new_result = Result.objects.create(
            session=new_session,
            section=new_section,
            created_at=result.created_at,
            question_key=result.question_key,
            is_profile=result.is_profile,
            expected_response=result.expected_response,
            given_response=result.given_response,
            comment=result.comment,
            score=result.score,
            scoring_rule=result.scoring_rule,
            json_data=result.json_data
        )
        new_result.save()

def get_or_create_playlist(playlist, apps, app_name='section'):
    Playlist = apps.get_model(app_name, 'Playlist')
    try:
        new_playlist = Playlist.objects.get(
            name=playlist.name
        )
    except Playlist.DoesNotExist:
        new_playlist = Playlist.objects.create(
            name=playlist.name,
            process_csv=playlist.process_csv,
            csv=playlist.csv
        )
        new_playlist.save()
    return new_playlist

def get_or_create_section(section, new_playlist, apps, app_name='section'):
    Section = apps.get_model(app_name, 'Section')
    try:
        new_section = Section.objects.get(
            filename=section.filename
        )
    except Section.DoesNotExist:
        new_section = Section.objects.create(
            playlist=new_playlist,
            artist=section.artist,
            name=section.name,
            start_time=section.start_time,
            duration=section.duration,
            filename=section.filename,
            restrict_to_nl=section.restrict_to_nl,
            play_count=section.play_count,
            code=section.code,
            tag=section.tag,
            group=section.group
        )
        new_section.save()
    return new_section

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
        playlist = session.playlist
        if playlist:
            playlist_app_name = app_name if app_name=='experiment' else 'section'
            new_playlist = get_or_create_playlist(playlist, apps, playlist_app_name)
        else:
            new_playlist = None
        new_session = Session.objects.create(
            experiment=session.experiment,
            participant=new_participant,
            playlist=new_playlist,
            started_at=session.started_at,
            finished_at=session.finished_at,
            json_data=session.json_data,
            final_score=session.final_score
        )
        new_session.save()
    return new_session    

def backwards_populate_results(apps, schema_editor):
    ExperimentResult = apps.get_model('experiment', 'Result')
    Result = apps.get_model('result', 'Result')
    for result in Result.objects.all():
        section = result.section
        if section:
            playlist = result.section.playlist
            new_playlist = get_or_create_playlist(playlist, apps, 'experiment')
            new_section = get_or_create_section(section, new_playlist, apps, 'experiment')
        else:
            new_section = None
        session = result.session
        participant = session.participant
        new_participant = get_or_create_participant(participant, apps, 'experiment')
        new_session = get_or_create_session(session, new_participant, apps, 'experiment')
        new_result = ExperimentResult.objects.create(
            session=new_session,
            section=new_section,
            created_at=result.created_at,
            question_key=result.question_key,
            is_profile=result.is_profile,
            expected_response=result.expected_response,
            given_response=result.given_response,
            comment=result.comment,
            score=result.score,
            scoring_rule=result.scoring_rule,
            json_data=result.json_data
        )
        new_result.save()


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0001_initial'),
        ('experiment', '0018_delete_profile'),
    ]

    operations = [
        migrations.RunPython(populate_results, backwards_populate_results)
    ]
