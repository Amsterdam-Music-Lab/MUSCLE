# Generated by Django 3.2.23 on 2024-01-26 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0005_section_add_validator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='restricted',
        ),
        migrations.AlterField(
            model_name='playlist',
            name='csv',
            field=models.TextField(blank=True, help_text='CSV Format: artist_name [string],        song_name [string], start_position [float], duration [float],        "path/filename.mp3" [string], tag [string], group [string]'),
        ),
    ]
