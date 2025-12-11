from django.db import migrations

def recreate_default_questions(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_add_custom_question_fields_and_modeltranslation'),
    ]

    operations = [
        migrations.RunPython(recreate_default_questions, reverse_code=migrations.RunPython.noop),
    ]
