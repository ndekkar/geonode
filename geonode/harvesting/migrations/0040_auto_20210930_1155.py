# Generated by Django 3.2.4 on 2021-09-30 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvesting', '0039_delete_harvestingsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvester',
            name='refresh_harvestable_resources_update_frequency',
            field=models.PositiveIntegerField(default=30, help_text='How often (in minutes) should new refresh sessions be automatically scheduled?'),
        ),
        migrations.AlterField(
            model_name='harvester',
            name='check_availability_frequency',
            field=models.PositiveIntegerField(default=10, help_text='How often (in minutes) should the remote service be checked for availability?'),
        ),
        migrations.AlterField(
            model_name='harvester',
            name='update_frequency',
            field=models.PositiveIntegerField(default=60, help_text='How often (in minutes) should new harvesting sessions be automatically scheduled?'),
        ),
    ]
