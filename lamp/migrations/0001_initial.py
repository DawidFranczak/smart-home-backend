# Generated by Django 5.1.1 on 2025-03-02 13:12

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lamp',
            fields=[
                ('device_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='device.device')),
                ('light_start', models.TimeField(default=datetime.datetime(2025, 3, 2, 14, 12))),
                ('light_stop', models.TimeField(default=datetime.datetime(2025, 3, 2, 14, 12))),
                ('brightness', models.SmallIntegerField(default=100)),
                ('step', models.SmallIntegerField(default=21)),
                ('lighting_time', models.SmallIntegerField(default=10)),
            ],
            bases=('device.device',),
        ),
    ]
