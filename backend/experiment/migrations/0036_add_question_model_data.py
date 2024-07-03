
from django.db import migrations
from experiment.models import Block as Experiment
from experiment.rules import EXPERIMENT_RULES


def add_default_question_series(apps, schema_editor):

    for experiment in Experiment.objects.all():
        if EXPERIMENT_RULES.get(experiment.rules) and not experiment.questionseries_set.all():
            experiment.add_default_question_series()


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0035_add_question_model'),
        ('question', '0002_add_question_model_data'),
    ]

    operations = [
        migrations.RunPython(add_default_question_series, reverse_code=migrations.RunPython.noop),
    ]
