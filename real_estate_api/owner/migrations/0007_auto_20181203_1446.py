# Generated by Django 2.0.6 on 2018-12-03 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0006_auto_20180806_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landlisting',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='landlisting',
            name='contact_number',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='landlisting',
            name='posted_by',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='contact_name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='contact_number',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='contact_profile_photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='posted_by',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='property_listing_type',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='propertylisting',
            name='property_type',
            field=models.CharField(max_length=250),
        ),
    ]