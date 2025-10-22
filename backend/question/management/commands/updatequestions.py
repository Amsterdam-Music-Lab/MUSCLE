from glob import glob

from django.core import serializers
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from question.models import Choice, Question

class Command(BaseCommand):
    help = 'Use to update the questions and choices defined in Python fixtures'

    def handle(self, *args, **options):
        # first, create choice sets which do not exist yet and set `from_python = True`
        update_choice_sets()
        # then create choices
        update_choices()
        # finally, create & update questions and set `from_python = True`
        update_questions()


def update_choice_sets():
    with open('/server/question/fixtures/choice_sets.yaml', 'r') as f:
        choice_sets = [obj.object for obj in serializers.deserialize('yaml', f)]
        for cs in choice_sets:
            cs.from_python = True
            cs.save()

def update_choices():
    for fixture in glob('/server/question/fixtures/choices_*.yaml'):
        with open(fixture, 'r') as f:
            choices = [obj.object for obj in serializers.deserialize('yaml', f)]
            for choice in choices:
                try:
                    choice.save()
                except IntegrityError:
                    existing = Choice.objects.get(key=choice.key, set=choice.set)
                    existing.text = choice.text
                    existing.index = choice.index
                    existing.save()

def update_questions():
    question_keys = []
    for fixture in glob('/server/question/fixtures/[!choice]*.yaml'):
        with open(fixture, 'r') as f:
            questions = [obj.object for obj in serializers.deserialize('yaml', f)]
            for question in questions:
                question.from_python = True
                try:
                    question.save()
                except IntegrityError:
                    Question.objects.get(key=question.key).delete()
                    question.save()
                question_keys.append(question.key)
    return question_keys
