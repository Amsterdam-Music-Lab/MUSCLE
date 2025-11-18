from django.db import migrations


def default_questions(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_add_question_model'),
    ]

    operations = [
        migrations.RunPython(default_questions, reverse_code=migrations.RunPython.noop),
    ]
