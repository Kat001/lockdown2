# Generated by Django 3.1 on 2021-05-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_auto_20210510_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='withdrawal_amount',
            field=models.FloatField(default=0),
        ),
    ]
