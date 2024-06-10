
from django.db import migrations
from question.questions import create_default_questions


def default_questions(apps, schema_editor):

    create_default_questions()


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_add_question_model'),
    ]

    operations = [
        migrations.RunPython(default_questions, reverse_code=migrations.RunPython.noop),
    ]
