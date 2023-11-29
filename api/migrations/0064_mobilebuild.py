# Generated by Django 3.0.8 on 2022-05-25 04:21

import api.custom_storage
import api.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_businesspermitapplication_is_renewal'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileBuild',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.CharField(blank=True, max_length=100)),
                ('file', models.FileField(null=True, storage=api.custom_storage.PrivateMediaStorage(), upload_to=api.models.MobileBuild.get_mobile_build_folder)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('for_maintenance', models.BooleanField(blank=True, default=True)),
                ('update_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
