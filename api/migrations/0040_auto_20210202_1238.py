# Generated by Django 3.0.8 on 2021-02-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_message_is_deliquent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_deliquent',
        ),
        migrations.AddField(
            model_name='thread',
            name='is_deliquent',
            field=models.BooleanField(default=False),
        ),
    ]
