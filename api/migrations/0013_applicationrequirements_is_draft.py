# Generated by Django 3.0.8 on 2021-01-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_applicationrequirements_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationrequirements',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
    ]
