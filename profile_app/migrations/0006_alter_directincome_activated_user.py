# Generated by Django 3.2 on 2021-04-28 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile_app', '0005_alter_directincome_activated_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directincome',
            name='activated_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activated_id', to=settings.AUTH_USER_MODEL),
        ),
    ]