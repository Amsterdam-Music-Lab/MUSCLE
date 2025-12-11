import json
import os
import subprocess
from typing import Union

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import activate, gettext

from question.models import Choice, Question

class Command(BaseCommand):
    """Command for populating translation fields of questions,
    using translations from Django .po files and unicode json files.
    The unicode json files will be skipped during tests.
    Usage: python manage.py translatequestions"""

    help = 'Populate translation fields of questions'

    def handle(self, *args, **options):
        if not getattr(settings, 'TESTING', False) and not os.path.isdir(
            "/unicode-translations/cldr-json"
        ):
            subprocess.run(
                [
                    "git",
                    "clone",
                    "-n",
                    "https://github.com/unicode-org/cldr-json/",
                    "--depth",
                    "1",
                    "/unicode-translations",
                ]
            )
        os.chdir("/unicode-translations")
        for lang in reversed(settings.MODELTRANSLATION_LANGUAGES):
            activate(lang)
            for question in Question.objects.all():
                set_attributes(question, ['text', 'explainer'])
                question.save()
            for choice in Choice.objects.exclude(
                choicelist__key__in=['ISO_COUNTRIES', 'ISO_LANGUAGES']
            ):
                set_attributes(choice, ['text'])
                choice.save()
            if not getattr(settings, 'TESTING', False):
                self.populate_iso_lists(lang)

    def populate_iso_lists(self, lang: str):
        try:
            lang_split = lang.split("-")
            lang_code = "-".join([lang_split[0], lang_split[1].capitalize()])
        except:
            lang_code = lang
        filepath = "cldr-json/cldr-localenames-full/main"
        subprocess.run(
            ["git", "checkout", "HEAD", f"{filepath}/{lang_code}/languages.json"]
        )
        subprocess.run(
            ["git", "checkout", "HEAD", f"{filepath}/{lang_code}/territories.json"]
        )
        with open(f"{filepath}/{lang_code}/territories.json") as f:
            data = json.load(f)
            countries = (
                data.get("main")
                .get(lang_code)
                .get("localeDisplayNames")
                .get("territories")
            )
        iso_country_choices = Choice.objects.filter(choicelist='ISO_COUNTRIES')
        for choice in iso_country_choices:
            country_key = next(
                (key for key in countries.keys() if key.lower() == choice.key)
            )
            if not country_key:
                continue
            setattr(choice, 'text', countries[country_key])
            choice.save()
        with open(f"{filepath}/{lang_code}/languages.json") as f:
            data = json.load(f)
            languages = (
                data.get("main")
                .get(lang_code)
                .get("localeDisplayNames")
                .get("languages")
            )
        iso_language_choices = Choice.objects.filter(choicelist='ISO_LANGUAGES')
        for choice in iso_language_choices:
            language_key = next(
                (key for key in languages.keys() if key.lower() == choice.key), None
            )
            if not language_key:
                continue
            setattr(choice, 'text', languages[language_key])
            choice.save()


def set_attributes(obj: Union[Question, Choice], fields: list[str]):
    for field in fields:
        translation = gettext(getattr(obj, field, ''))
        setattr(obj, field, translation)
