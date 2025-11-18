from django.db import migrations
from experiment.rules import BLOCK_RULES as EXPERIMENT_RULES


def add_default_question_series(apps, schema_editor):
    pass



class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0035_add_question_model'),
        ('question', '0002_add_question_model_data'),
    ]

    operations = [
        migrations.RunPython(add_default_question_series, reverse_code=migrations.RunPython.noop),
    ]
