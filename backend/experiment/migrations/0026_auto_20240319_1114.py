# Generated by Django 3.2.24 on 2024-03-19 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0025_auto_20240313_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentseries',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='experimentseries',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]
