# Generated by Django 3.0.8 on 2021-06-30 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20210621_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='landbanktransaction',
            name='date_stamp',
            field=models.DateTimeField(null=True),
        ),
    ]