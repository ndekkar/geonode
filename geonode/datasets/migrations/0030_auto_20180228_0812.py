# Generated by Django 1.9.13 on 2018-02-28 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0030_auto_20171212_0518'),
        ('datasets', '0029_layer_service'),
    ]
    try:
        from django.db.migrations.recorder import MigrationRecorder
        is_fake = MigrationRecorder.Migration.objects.filter(app='layers', name='0030_auto_20180228_0812')
        is_fake_migration = is_fake.exists()
    except Exception:
        is_fake_migration = False

    if is_fake_migration:
        is_fake.update(app='datasets')
    else:
        operations = [
            migrations.RemoveField(
                model_name='Dataset',
                name='service',
            ),
            migrations.AddField(
                model_name='Dataset',
                name='remote_service',
                field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.Service'),
            ),
        ]
