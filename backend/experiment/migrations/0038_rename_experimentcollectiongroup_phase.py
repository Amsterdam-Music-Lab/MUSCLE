# Generated by Django 3.2.25 on 2024-06-19 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0037_experimentcollection_active'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExperimentCollectionGroup',
            new_name='Phase',
        ),
    ]