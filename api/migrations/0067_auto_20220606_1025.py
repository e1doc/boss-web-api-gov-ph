# Generated by Django 3.0.8 on 2022-06-06 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_mobiledownloads'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MobileDownloads',
            new_name='MobileDownload',
        ),
        migrations.RenameField(
            model_name='mobiledownload',
            old_name='user',
            new_name='user_email',
        ),
    ]
