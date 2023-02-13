from django.db import migrations, models

def apply_sections(apps, from_app, to_app):
    ''' create sections and playlists
    delete old ones when done '''
    OldSection = apps.get_model(from_app, 'Section')
    NewSection = apps.get_model(to_app, 'Section')
    for section in OldSection.objects.all():
        new_playlist = get_or_create_playlist(section.playlist, apps, to_app)
        new_section = NewSection.objects.create(
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

def get_or_create_playlist(playlist, apps, to_app):
    Playlist = apps.get_model(to_app, 'Playlist')
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

def change_playlist_reference(apps, schema_editor):
    apply_changes(apps, 'experiment', 'section')

def backwards_change_playlist_reference(apps, schema_editor):
    apply_changes(apps, 'section', 'experiment')

def apply_changes(apps, from_app, to_app):
    Experiment = apps.get_model('experiment', 'Experiment')
    # first create sections and playlists
    apply_sections(apps, from_app, to_app)
    for exp in Experiment.objects.all():
        for playlist in exp.playlists.all():
            new_playlist = get_playlist(playlist, apps, to_app)
            if to_app=='section':
                # use temporary field to add the playlist
                exp.tmp_playlists.add(new_playlist)
            else:
                exp.playlists.add(new_playlist)
            exp.save()

def get_playlist(playlist, apps, app_name='section'):
    Playlist = apps.get_model(app_name, 'Playlist')
    return Playlist.objects.get(
        name=playlist.name
    )

class Migration(migrations.Migration):

    dependencies = [
        ('section', '0001_initial'),
        ('experiment', '0012_participant_access_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='tmp_playlists',
            field=models.ManyToManyField(to='section.Playlist')
        ),
        migrations.RunPython(change_playlist_reference, backwards_change_playlist_reference),
        migrations.RemoveField(
            model_name='experiment',
            name='playlists',
            field=models.ManyToManyField(to='experiment.Playlist')
        ),
        migrations.RenameField(
            model_name='experiment',
            old_name='tmp_playlists',
            new_name='playlists'
        )
    ]
