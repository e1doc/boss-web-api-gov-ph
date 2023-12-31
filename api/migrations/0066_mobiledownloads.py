# Generated by Django 3.0.8 on 2022-06-06 10:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_auto_20220525_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileDownloads',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.CharField(blank=True, max_length=100)),
                ('version', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
