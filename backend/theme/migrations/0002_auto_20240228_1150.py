# Generated by Django 3.2.24 on 2024-02-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='themeconfig',
            old_name='font_url',
            new_name='body_font_url',
        ),
        migrations.AddField(
            model_name='themeconfig',
            name='heading_font_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
