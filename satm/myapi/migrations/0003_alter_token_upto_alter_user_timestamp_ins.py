# Generated by Django 4.2.13 on 2024-07-03 19:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_alter_token_upto_alter_user_timestamp_ins_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='UPTO',
            field=models.IntegerField(default='2024-07-03T20:00:33.110926'),
        ),
        migrations.AlterField(
            model_name='user',
            name='TIMESTAMP_INS',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 3, 19, 0, 33, 111208)),
        ),
    ]
