# Generated by Django 2.2.11 on 2020-06-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0072_auto_20200604_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcebase',
            name='embrapa_unity',
            field=models.CharField(default='96', help_text='Escolha a unidade da Embrapa', max_length=20, verbose_name='embrapa unity'),
        ),
    ]
