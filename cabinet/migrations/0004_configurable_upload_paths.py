# Generated by Django 2.1 on 2018-08-25 11:16

import cabinet.base
from django.db import migrations, models
import imagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("cabinet", "0004_auto_20181212_0252"),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='download_file',
            field=models.FileField(blank=True, upload_to=cabinet.base.downloads_upload_path, verbose_name='download'),
        ),
        migrations.AlterField(
            model_name='file',
            name='image_file',
            field=imagefield.fields.ImageField(blank=True, height_field='image_height', upload_to=cabinet.base.images_upload_path, verbose_name='image', width_field='image_width'),
        ),
    ]
