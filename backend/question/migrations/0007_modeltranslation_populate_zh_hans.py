from django.db import migrations
from question.questions import create_default_questions
from question import questions
from django.core import management
from django.utils import translation


def populate_translation_fields(apps, schema_editor):

    QuestionH = apps.get_model("question", "Question")
    questions.populate_translation_fields("zh-hans", question_model=QuestionH)


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_modeltranslation_add_language_zh_hans'),
    ]

    operations = [
        migrations.RunPython(populate_translation_fields, reverse_code=migrations.RunPython.noop),
    ]






    
