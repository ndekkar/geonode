# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0033_auto_20180414_2120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelManagers(
            name='document',
            managers=[
            ],
        ),
    ]
