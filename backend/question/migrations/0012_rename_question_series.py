from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0011_rename_question_question_text'),
    ]

    operations = [
        migrations.RenameModel('QuestionSeries', 'QuestionList'),
        migrations.RenameModel('QuestionInSeries', 'QuestionInList'),
        migrations.RenameField('QuestionInList', 'question_series', 'questionlist'),
    ]
