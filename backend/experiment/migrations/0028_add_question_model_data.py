
from django.db import migrations
from experiment.models import Experiment
from experiment.questions import create_default_questions


def add_default_question_series(apps, schema_editor):

    create_default_questions()

    for experiment in Experiment.objects.all():
        experiment.add_default_question_series()


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0027_add_question_model'),
    ]

    operations = [
        migrations.RunPython(add_default_question_series, reverse_code=migrations.RunPython.noop),
    ]
