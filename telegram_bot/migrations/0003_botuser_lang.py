# Generated by Django 3.1.7 on 2021-03-10 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_auto_20210310_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='lang',
            field=models.CharField(default='uz', max_length=10),
        ),
    ]
