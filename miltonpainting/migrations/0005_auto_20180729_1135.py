# Generated by Django 2.0.7 on 2018-07-29 15:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('miltonpainting', '0004_auto_20180729_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paintestimate',
            name='date_time',
        ),
        migrations.AddField(
            model_name='paintestimateuser',
            name='date_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]