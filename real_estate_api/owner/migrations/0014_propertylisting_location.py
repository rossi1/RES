# Generated by Django 2.0 on 2018-12-24 20:37

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0013_remove_propertylisting_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertylisting',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(geography=True, null=True, srid=4326),
        ),
    ]