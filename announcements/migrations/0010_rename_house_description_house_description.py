# Generated by Django 4.2.2 on 2023-06-11 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0009_remove_house_image_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='house_description',
            new_name='description',
        ),
    ]
