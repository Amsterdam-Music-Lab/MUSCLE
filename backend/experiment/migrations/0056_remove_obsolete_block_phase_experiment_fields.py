# Generated by Django 4.2.15 on 2024-09-10 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0055_remove_block_consent_remove_block_hashtag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='active',
        ),
        migrations.RemoveField(
            model_name='block',
            name='description',
        ),
        migrations.RemoveField(
            model_name='block',
            name='name',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='dashboard',
        ),
        migrations.RemoveField(
            model_name='phase',
            name='name',
        ),
    ]