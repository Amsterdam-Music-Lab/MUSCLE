from django.db import migrations
from question.questions import create_default_questions


def recreate_default_questions(apps, schema_editor):
    create_default_questions(overwrite=True)


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_add_custom_question_fields_and_modeltranslation'),
    ]

    operations = [
        migrations.RunPython(recreate_default_questions, reverse_code=migrations.RunPython.noop),
    ]






    
