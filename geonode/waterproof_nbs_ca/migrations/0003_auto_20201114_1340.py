# Generated by Django 2.2.16 on 2020-11-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterproof_nbs_ca', '0002_auto_20201113_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterproofnbsca',
            name='max_benefit_req_time',
            field=models.IntegerField(default=0, verbose_name='Time maximum benefit'),
        ),
    ]
