# Generated by Django 3.1.7 on 2021-03-10 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0003_botuser_lang'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'get_latest_by': 'id', 'verbose_name': 'Buyurtma', 'verbose_name_plural': 'Buyurtmalar'},
        ),
    ]
