# Generated by Django 3.0.8 on 2021-01-14 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20210114_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdetails',
            name='complete_business_address',
            field=models.TextField(blank=True),
        ),
    ]