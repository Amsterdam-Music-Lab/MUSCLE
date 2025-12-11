from django.db import migrations

def populate_translation_fields(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_modeltranslation_add_language_zh_hans'),
    ]

    operations = [
        migrations.RunPython(populate_translation_fields, reverse_code=migrations.RunPython.noop),
    ]
