# Generated by Django 3.1.7 on 2021-03-11 11:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0010_auto_20210311_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 11, 16, 19, 40, 977696)),
        ),
    ]
