# Generated by Django 3.1 on 2021-05-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0020_auto_20210511_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedpackages',
            name='days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]