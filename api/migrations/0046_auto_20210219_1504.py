# Generated by Django 3.0.8 on 2021-02-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20210219_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='landbanktransaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='landbanktransaction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
