# Generated by Django 3.1.4 on 2020-12-07 17:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 7, 17, 16, 42, 575942, tzinfo=utc), verbose_name='Date Joined'),
        ),
    ]
