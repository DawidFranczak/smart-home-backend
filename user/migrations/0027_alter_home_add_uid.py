# Generated by Django 5.1.1 on 2025-03-27 16:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0026_alter_home_add_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="home",
            name="add_uid",
            field=models.UUIDField(
                default=uuid.UUID("453b45e4-8247-4615-8dba-3be6df07d296")
            ),
        ),
    ]
