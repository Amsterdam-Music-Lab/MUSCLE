import json
import os
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import activate

from question.models import Choice

class Command(BaseCommand):
    """Command for populating translation fields of questions
    Usage: python manage.py translatequestions"""

    help = 'Populate translation fields of questions'

    def handle(self, *args, **options):
        if not os.path.isdir("cldr-json"):
            subprocess.run(
                [
                    "git",
                    "clone",
                    "-n",
                    "https://github.com/unicode-org/cldr-json/",
                    "--depth",
                    "1",
                ]
            )
        os.chdir("cldr-json")
        for lang in reversed(settings.MODELTRANSLATION_LANGUAGES):
            activate(lang)
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
        iso_country_questions = [
            'dgf_country_of_origin',
            'dgf_country_of_residence',
        ]
        for question_key in iso_country_questions:
            choices = Choice.objects.filter(question__key=question_key)
            for choice in choices:
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
        choices = Choice.objects.filter(question__key='dgf_native_language')
        for choice in choices:
            language_key = next(
                (key for key in languages.keys() if key.lower() == choice.key), None
            )
            if not language_key:
                continue
            setattr(choice, 'text', languages[language_key])
            choice.save()
