from django.db import migrations

def populate_participants(apps, schema_editor):
    ExperimentParticipant = apps.get_model('experiment', 'Participant')
    Participant = apps.get_model('participant', 'Participant')
    for original_participant in ExperimentParticipant.objects.all():
        new_participant = Participant.objects.create(
            unique_hash=original_participant.unique_hash,
            country_code=original_participant.country_code,
            access_info=original_participant.access_info
        )
        new_participant.save()

def backwards_populate_participants(apps, schema_editor):
    ExperimentParticipant = apps.get_model('experiment', 'Participant')
    Participant = apps.get_model('participant', 'Participant')
    for new_participant in Participant.objects.all():
        original_participant = ExperimentParticipant.objects.create(
            unique_hash=new_participant.unique_hash,
            country_code=new_participant.country_code,
            access_info=new_participant.access_info
        )
        original_participant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
        ('experiment', '0012_participant_access_info'),
    ]

    operations = [
        migrations.RunPython(populate_participants, backwards_populate_participants)
    ]
