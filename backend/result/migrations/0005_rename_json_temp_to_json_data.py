# Generated by Django 3.2.20 on 2023-11-24 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0004_migrate_json_data_to_JSONField'),
    ]

    operations = [
        migrations.RenameField(
            model_name='Result',
            old_name='json_data',
            new_name='old_data'
        ),
        migrations.RenameField(
            model_name='Result',
            old_name='json_temp',
            new_name='json_data'
        )
    ]
