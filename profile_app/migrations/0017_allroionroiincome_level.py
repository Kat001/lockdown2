# Generated by Django 3.2 on 2021-05-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0016_allroionroiincome'),
    ]

    operations = [
        migrations.AddField(
            model_name='allroionroiincome',
            name='level',
            field=models.CharField(default='', max_length=5),
        ),
    ]
