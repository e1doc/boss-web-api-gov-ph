# Generated by Django 3.0.8 on 2021-01-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_businesspermitapplication_on_renewal'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationrequirements',
            name='remarks_draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='businessactivity',
            name='remarks_draft',
            field=models.BooleanField(default=False),
        ),
    ]
