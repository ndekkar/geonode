# Generated by Django 3.2.4 on 2021-09-22 10:27

from django.db import migrations


def update_geonode_harvester_module_name(apps, schema_editor):
    harvester_model = apps.get_model("harvesting", "Harvester")
    old_module_name = "geonode"
    new_module_name = "geonodeharvester"
    fragment_pattern = "geonode.harvesting.harvesters.{module}."
    old_path_fragment = fragment_pattern.format(module=old_module_name)
    new_path_fragment = fragment_pattern.format(module=new_module_name)
    for harvester in harvester_model.objects.filter(harvester_type__startswith=old_path_fragment):
        harvester.harvester_type = harvester.harvester_type.replace(old_path_fragment, new_path_fragment)
        harvester.save()


class Migration(migrations.Migration):

    dependencies = [
        ('harvesting', '0034_harvester_unique name'),
    ]

    operations = [
        migrations.RunPython(update_geonode_harvester_module_name)
    ]
