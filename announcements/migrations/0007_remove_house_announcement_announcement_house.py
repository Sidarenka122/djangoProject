# Generated by Django 4.2.2 on 2023-06-11 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0006_alter_announcement_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='announcement',
        ),
        migrations.AddField(
            model_name='announcement',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='announcements.house'),
        ),
    ]
