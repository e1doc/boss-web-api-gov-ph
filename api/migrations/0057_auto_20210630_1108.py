# Generated by Django 3.0.8 on 2021-06-30 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_landbanktransaction_date_stamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingbasicinformation',
            name='owner_complete_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='barangay',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='character_of_occupancy',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='character_of_occupancy_others',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='subdivision_name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='businessbasicinformation',
            name='owner_complete_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='businessdetails',
            name='barangay',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='businessdetails',
            name='subdivision',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='lessordetails',
            name='complete_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='lessordetails',
            name='telephone_number',
            field=models.TextField(blank=True),
        ),
    ]
