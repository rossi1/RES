# Generated by Django 2.0 on 2018-12-24 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0012_auto_20181223_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertylisting',
            name='location',
        ),
    ]
