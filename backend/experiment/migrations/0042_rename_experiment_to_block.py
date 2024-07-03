from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0041_socialmediaconfig'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Experiment',
            new_name='Block',
        ),
        migrations.RenameField(
            model_name='groupedexperiment',
            old_name='experiment',
            new_name='block',
        )
    ]
