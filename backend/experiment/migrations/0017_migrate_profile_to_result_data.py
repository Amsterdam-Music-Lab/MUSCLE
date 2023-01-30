from django.db import migrations

def move_profile_to_result(apps, schema_editor):
    Profile = apps.get_model('experiment', 'Profile')
    Result = apps.get_model('experiment', 'Result')
    Session = apps.get_model('experiment', 'Session')
    sessions_created = 0
    for profile in Profile.objects.all():
        # retrieve or create Session object
        try:
            linked_session = Session.objects.filter(
                participant=profile.participant,
                experiment=None
            ).first()
        except Session.DoesNotExist:
            linked_session = Session.objects.create(
                participant=profile.participant
            )
            linked_session.save()
            sessions_created += 1
        result = Result.objects.create(
            session=linked_session,
            question_key=profile.question,
            created_at=profile.created_at,
            is_profile=True,
            given_response=profile.answer,
            score=profile.score
        )
        result.save()

def move_result_to_profile(apps, schema_editor):
    Profile = apps.get_model('experiment', 'Profile')
    Result = apps.get_model('experiment', 'Result')
    for result in Result.objects.filter(is_profile=True):
        profile = Profile.objects.create(
            participant=result.session.participant,
            created_at=result.created_at,
            question=result.question_key,
            answer=result.given_response,
            session_id=result.session.id,
            score=result.score
        )
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0016_result_profile_scoring_rule'),
    ]

    operations = [
        migrations.RunPython(move_profile_to_result, move_result_to_profile)
    ]
