# Generated by Django 3.2.24 on 2024-02-20 09:32

import django.core.validators
from django.db import migrations, models
import experiment.models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0018_set_default_question_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experimentseries',
            options={'verbose_name_plural': 'Experiment Series'},
        ),
        migrations.AddField(
            model_name='experiment',
            name='consent',
            field=models.FileField(blank=True, default='', upload_to=experiment.models.consent_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['md', 'html'])]),
        ),
    ]
