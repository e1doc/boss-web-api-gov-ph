# Generated by Django 3.0.8 on 2021-01-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20210114_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdetails',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='businessdetails',
            name='trade_name',
            field=models.TextField(blank=True),
        ),
    ]
