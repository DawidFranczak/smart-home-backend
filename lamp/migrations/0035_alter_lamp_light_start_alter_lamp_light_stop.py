# Generated by Django 5.1.1 on 2025-05-01 10:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lamp", "0034_alter_lamp_light_start_alter_lamp_light_stop"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lamp",
            name="light_start",
            field=models.TimeField(default=datetime.datetime(2025, 5, 1, 12, 48)),
        ),
        migrations.AlterField(
            model_name="lamp",
            name="light_stop",
            field=models.TimeField(default=datetime.datetime(2025, 5, 1, 12, 48)),
        ),
    ]
