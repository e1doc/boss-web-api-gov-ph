# Generated by Django 3.0.8 on 2021-01-26 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_banktransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='soa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Soa'),
        ),
    ]