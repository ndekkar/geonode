# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0026_auto_20190429_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maplayer',
            name='format',
            field=models.TextField(blank=True, null=True, verbose_name='format'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='group',
            field=models.TextField(blank=True, null=True, verbose_name='group'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='name',
            field=models.TextField(null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='styles',
            field=models.TextField(blank=True, null=True, verbose_name='styles'),
        ),
    ]
