# Generated by Django 5.1.1 on 2025-04-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0017_event_event_alter_event_device"),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="is_online",
            field=models.BooleanField(default=True),
        ),
    ]
