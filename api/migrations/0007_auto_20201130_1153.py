# Generated by Django 3.0.8 on 2020-11-30 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_message_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingbasicinformation',
            name='owner_first_name',
            field=models.TextField(blank=True),
        ),
    ]
