# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-09 12:38

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0027_auto_20180302_0430'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='map',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
