from django.db import migrations

from question.management.commands.updatequestions import (
    update_choices,
    update_choice_lists,
    update_questions,
)


def flip_boolean_sign(apps, schema_editor):
    """since the previous migration renamed `question.editable` to `question.from_python`,
    the meaning of the boolean value is reversed: True means *not* editable
    """
    QuestionModel = apps.get_model('question.Question')
    for question in QuestionModel.objects.all():
        question.from_python = not question.from_python
        question.save()


def choice_to_choice_list(apps, schema_editor):
    """import the Python defined questions from fixtures, and update all other questions"""
    ChoiceModel = apps.get_model("question.Choice")
    ChoiceListModel = apps.get_model("question.ChoiceList")
    QuestionModel = apps.get_model("question.Question")
    update_choice_lists()
    update_choices()
    python_defined_questions = update_questions()
    for question in QuestionModel.objects.exclude(key__in=python_defined_questions):
        if hasattr(question, 'choice_set'):
            cl, has_created_choice_list = ChoiceListModel.objects.get_or_create(
                key=f"{question.key}_choices"
            )
            for choice in question.choice_set.all():
                choice.choicelist = cl
                if has_created_choice_list:
                    question.choices = cl
                    question.save()
                try:
                    choice.save()
                except:
                    choice.delete()  # we have more choices in the choice->question setup
    ChoiceModel.objects.filter(
        choicelist__isnull=True
    ).delete()  # to be safe, delete choices without choice list


def choice_to_question(apps, schema_editor):
    ChoiceModel = apps.get_model("question.Choice")
    ChoiceListModel = apps.get_model("question.ChoiceList")
    QuestionModel = apps.get_model("question.Question")
    for question in QuestionModel.objects.all():
        choice_list = getattr(question, 'choices', None)
        if choice_list:
            ChoiceModel.objects.bulk_create(
                [
                    ChoiceModel(
                        question=question,
                        key=choice.key,
                        text=choice.text,
                        index=choice.index,
                    )
                    for choice in choice_list.choices.all()
                ]
            )
    ChoiceListModel.objects.all().delete()  # to ensure we leave no dangling choices


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0012_rename_question_series'),
    ]

    operations = [
        migrations.RunPython(choice_to_choice_list, reverse_code=choice_to_question),
        migrations.RunPython(migrations.RunPython.noop, reverse_code=flip_boolean_sign),
    ]
