from django.db import migrations
from question.questions import create_default_questions
from question.models import QuestionInSeries, Question
from django.core import management
from django.utils import translation
import modeltranslation

def recreate_default_questions(apps, schema_editor):

    QuestionH = apps.get_model("question", "Question")
    ChoiceH = apps.get_model("question", "Choice")
    QuestionGroupH = apps.get_model("question", "QuestionGroup")
    QuestionInSeriesH = apps.get_model("question", "QuestionInSeries")

    # Save info of all QuestionInSeries objects, because they will be deleted when recreating questions
    qis_all = QuestionInSeriesH.objects.all()
    qis_all_list = []
    for qis in qis_all:
        qis_all_list.append({'question_series':qis.question_series, "question_key":qis.question.key, "index":qis.index})

    # Delete old default questions
    QuestionH.objects.all().delete()

    create_default_questions(question_model=QuestionH, choice_model=ChoiceH, question_group_model=QuestionGroupH)

    # Recreate QuestionInSeries objects with new question objects
    for qis in qis_all_list:
        QuestionInSeriesH.objects.create(
            question_series=qis["question_series"],
            question=QuestionH.objects.get(key=qis["question_key"]),
            index=qis["index"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_add_custom_question_fields_and_modeltranslation'),
    ]

    operations = [
        migrations.RunPython(recreate_default_questions, reverse_code=migrations.RunPython.noop),
    ]






    
