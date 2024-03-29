# Generated by Django 3.2.12 on 2022-04-28 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0006_rename_experiment_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='csv',
            field=models.TextField(blank=True, help_text='CSV Format: artist_name [string],        song_name [string], start_position [float], duration [float],        "path/filename.mp3" [string], restricted_to_nl [int 0=False 1=True], tag_id [string], group_id [string]'),
        ),
        migrations.AlterField(
            model_name='section',
            name='group_id',
            field=models.CharField(default='0', max_length=128),
        ),
        migrations.AlterField(
            model_name='section',
            name='tag_id',
            field=models.CharField(default='0', max_length=128),
        ),
    ]
