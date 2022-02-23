# Generated by Django 3.2.12 on 2022-02-23 14:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('upload', '0036_upload_store_spatial_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadParallelismLimit',
            fields=[
                ('slug', models.SlugField(blank=True, max_length=255, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
                ('description', models.TextField(blank=True, default=None, max_length=255, null=True)),
                ('max_number', models.PositiveSmallIntegerField(default=5, help_text='The maximum number of parallel uploads (0 to 32767).')),
                ('group', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('slug',),
            },
        ),
    ]
