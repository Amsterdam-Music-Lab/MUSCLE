from django.core.management import call_command
from django.test import TestCase
import csv
from django.conf import settings
from os.path import join
from os import remove
 

class CompilePlaylistTest(TestCase):

    def test_output_csv(self):
        call_command('compileplaylist', 'tests/compileplaylist')
        # Load generated csv
        filename = join(settings.MEDIA_ROOT,'tests','compileplaylist','audiofiles.csv')
        try:
            with open(filename) as csv_file:
                rows = csv.DictReader(csv_file, fieldnames = ('artist','name','start_time','duration','filename','tag','group'))
                for row in rows:
                    if row['filename'] == 'tests/compileplaylist/silence_20sec.wav':
                        self.assertEqual(row['artist'], 'default')
                        self.assertEqual(row['name'], 'silence_20sec')
                        self.assertEqual(row['start_time'], '0.0')
                        self.assertEqual(row['duration'], '20.025850340136053')
                        self.assertEqual(row['tag'], '0')
                        self.assertEqual(row['group'], '0')
        finally:        
            remove(filename)  # Make sure csv file is deleted even if tests fail

    def test_createquestions(self):
        from question.models import Question, QuestionGroup
        call_command('createquestions')
        self.assertEqual(len(Question.objects.all()), 161) # Only built-in questions in test database
        self.assertEqual(len(QuestionGroup.objects.all()), 18) # Only built-in question groups in test database
        self.assertEqual(len(Question.objects.filter(key='dgf_country_of_origin')), 1)
        self.assertEqual(len(QuestionGroup.objects.filter(key='DEMOGRAPHICS')), 1)


