# Generated by Django 5.1.1 on 2025-03-13 17:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_home_add_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='add_uid',
            field=models.UUIDField(default=uuid.UUID('d7933643-293d-4010-a445-c0a488486384')),
        ),
    ]
