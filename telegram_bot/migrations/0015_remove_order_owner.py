# Generated by Django 3.1.7 on 2021-03-11 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0014_order_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='owner',
        ),
    ]
