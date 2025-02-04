# Generated by Django 4.2.16 on 2024-11-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_recreate_default_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='text_zh_hans',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='explainer_zh_hans',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_zh_hans',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
