# Generated by Django 3.1.1 on 2020-09-23 06:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0005_auto_20200923_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
