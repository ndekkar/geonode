# Generated by Django 3.2.7 on 2021-10-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvesting', '0040_merge_20211001_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvestableresource',
            name='abstract',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]
