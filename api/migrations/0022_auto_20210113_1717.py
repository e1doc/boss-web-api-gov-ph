# Generated by Django 3.0.8 on 2021-01-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20210113_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessactivity',
            name='units',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]