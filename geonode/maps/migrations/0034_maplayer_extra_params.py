# Generated by Django 3.2.7 on 2021-11-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0033_convert_map_blob'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='extra_params',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
