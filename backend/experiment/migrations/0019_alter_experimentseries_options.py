# Generated by Django 3.2.23 on 2023-12-17 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0018_set_default_question_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experimentseries',
            options={'verbose_name_plural': 'Experiment Series'},
        ),
    ]