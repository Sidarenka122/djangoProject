# Generated by Django 4.2.2 on 2023-06-11 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_alter_announcement_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='views',
            field=models.CharField(editable=False, max_length=255),
        ),
    ]