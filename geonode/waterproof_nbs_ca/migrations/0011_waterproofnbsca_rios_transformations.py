# Generated by Django 2.2.16 on 2020-12-03 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_nbs_ca', '0010_auto_20201203_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterproofnbsca',
            name='rios_transformations',
            field=models.ManyToManyField(to='waterproof_nbs_ca.RiosTransformation'),
        ),
    ]
