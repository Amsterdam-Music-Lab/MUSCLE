# Generated by Django 3.2.20 on 2023-11-23 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0002_data_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='json_temp',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
