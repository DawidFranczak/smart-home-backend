# Generated by Django 5.1.1 on 2025-03-15 16:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0016_alter_home_add_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="home",
            name="add_uid",
            field=models.UUIDField(
                default=uuid.UUID("70d7fa80-0eb6-4dcb-8f4c-835f3e4ec27c")
            ),
        ),
    ]
