# Generated by Django 3.2.8 on 2021-11-02 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='nested_experiments',
            field=models.JSONField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='csv',
            field=models.TextField(blank=True, help_text='CSV Format: artist_name [string], song_name [string], start_position [float], duration [float], "path/filename.mp3" [string], restricted_to_nl [int 0=False 1=True], tag_id [int], group_id [int]'),
        ),
    ]
