from django.db import migrations

from question.management.commands.updatequestions import (
    update_choices,
    update_choice_sets,
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


def choice_to_choice_set(apps, schema_editor):
    """import the Python defined questions from fixtures, and update all other questions"""
    ChoiceModel = apps.get_model("question.Choice")
    ChoiceSetModel = apps.get_model("question.ChoiceSet")
    QuestionModel = apps.get_model("question.Question")
    update_choice_sets()
    update_choices()
    python_defined_questions = update_questions()
    for question in QuestionModel.objects.exclude(key__in=python_defined_questions):
        if hasattr(question, 'choice_set'):
            cs, has_created_choice_set = ChoiceSetModel.objects.get_or_create(
                key=f"{question.key}_choices"
            )
            for choice in question.choice_set.all():
                choice.set = cs
                if has_created_choice_set:
                    question.choices = cs
                    question.save()
                try:
                    choice.save()
                except:
                    choice.delete()  # we have more choices in the choice->question setup
    ChoiceModel.objects.filter(
        set__isnull=True
    ).delete()  # to be safe, delete choices without choice set


def choice_to_question(apps, schema_editor):
    ChoiceModel = apps.get_model("question.Choice")
    ChoiceSetModel = apps.get_model("question.ChoiceSet")
    QuestionModel = apps.get_model("question.Question")
    for question in QuestionModel.objects.all():
        choice_set = getattr(question, 'choices', None)
        if choice_set:
            ChoiceModel.objects.bulk_create(
                [
                    ChoiceModel(
                        question=question,
                        key=choice.key,
                        text=choice.text,
                        index=choice.index,
                    )
                    for choice in choice_set.choices.all()
                ]
            )
    ChoiceSetModel.objects.all().delete()  # to ensure we leave no dangling choices


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0011_rename_question_question_text'),
    ]

    operations = [
        migrations.RunPython(choice_to_choice_set, reverse_code=choice_to_question),
        migrations.RunPython(migrations.RunPython.noop, reverse_code=flip_boolean_sign),
    ]
