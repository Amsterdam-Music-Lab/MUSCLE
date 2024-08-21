from django.db import migrations
from question.questions import create_default_questions
from question.models import QuestionInSeries, Question


def recreate_default_questions(apps, schema_editor):

    # Save info of all QuestionInSeries objects, because they will be deleted when recreating questions
    qis_all = QuestionInSeries.objects.all()
    qis_all_list = []
    for qis in qis_all:
        qis_all_list.append({'question_series':qis.question_series, "question_key":qis.question.key, "index":qis.index})

    create_default_questions(overwrite=True)

    # Recreate QuestionInSeries objects with new question objects
    for qis in qis_all_list:
        QuestionInSeries.objects.create(
            question_series=qis["question_series"],
            question=Question.objects.get(key=qis["question_key"]),
            index=qis["index"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_add_custom_question_fields_and_modeltranslation'),
    ]

    operations = [
        migrations.RunPython(recreate_default_questions, reverse_code=migrations.RunPython.noop),
    ]






    
