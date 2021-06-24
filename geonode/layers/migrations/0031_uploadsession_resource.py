# Generated by Django 1.11.11 on 2018-04-24 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_auto_20180330_0951'),
        ('layers', '0030_auto_20180228_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadsession',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ResourceBase'),
        ),
    ]
