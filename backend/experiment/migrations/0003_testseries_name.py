# Generated by Django 3.2.8 on 2021-12-17 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0002_test_series_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='testseries',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]
