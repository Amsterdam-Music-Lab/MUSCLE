from django.db import migrations
from question.questions import create_default_questions
from question import questions


def populate_translation_fields(apps, schema_editor):
    questions.populate_translation_fields("zh-hans")

class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_modeltranslation_add_language_zh_hans'),
    ]

    operations = [
        migrations.RunPython(populate_translation_fields, reverse_code=migrations.RunPython.noop),
    ]






    
