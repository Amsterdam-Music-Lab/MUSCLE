
from django.core.management.base import BaseCommand

from question.questions import create_default_questions


class Command(BaseCommand):
	help = "Creates default questions and question groups in the database"

	def handle(self, *args, **options):
		create_default_questions()
