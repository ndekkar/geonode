# Generated by Django 3.2 on 2021-06-11 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0066_resourcebase_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resourcebase',
            old_name='blob',
            new_name='data',
        ),
    ]
