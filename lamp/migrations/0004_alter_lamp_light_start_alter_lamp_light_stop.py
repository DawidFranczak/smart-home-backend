# Generated by Django 5.1.1 on 2025-03-02 16:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lamp', '0003_alter_lamp_light_start_alter_lamp_light_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lamp',
            name='light_start',
            field=models.TimeField(default=datetime.datetime(2025, 3, 2, 17, 3)),
        ),
        migrations.AlterField(
            model_name='lamp',
            name='light_stop',
            field=models.TimeField(default=datetime.datetime(2025, 3, 2, 17, 3)),
        ),
    ]
