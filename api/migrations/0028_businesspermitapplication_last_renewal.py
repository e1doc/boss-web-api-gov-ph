# Generated by Django 3.0.8 on 2021-01-15 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20210114_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesspermitapplication',
            name='last_renewal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]