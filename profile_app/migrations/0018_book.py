# Generated by Django 3.2 on 2021-05-05 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0017_allroionroiincome_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('thumbnail', models.ImageField(upload_to='thumbnails')),
                ('trailer', models.FileField(upload_to='Videos')),
            ],
        ),
    ]
