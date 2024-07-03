from django.db import migrations
from experiment.rules import BLOCK_RULES as EXPERIMENT_RULES


def set_default_question_data(apps, schema_editor):

    Experiment = apps.get_model("experiment", "Experiment")

    for experiment in Experiment.objects.all():
        experiment.questions = [q.key for q in EXPERIMENT_RULES[experiment.rules]().questions]
        experiment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0017_experiment_add_questions_field'),
    ]

    operations = [
        migrations.RunPython(set_default_question_data, reverse_code=migrations.RunPython.noop),
    ]
