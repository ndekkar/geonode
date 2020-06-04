# Generated by Django 2.2.11 on 2020-06-03 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0068_auto_20200603_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embrapa_Last_Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('last_updated',),
            },
        ),
    ]
