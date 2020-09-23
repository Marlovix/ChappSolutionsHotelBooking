# Generated by Django 3.1.1 on 2020-09-19 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TypeRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_guest', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=2)),
                ('type_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelBooking.typeroom')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('n_guest', models.IntegerField()),
                ('nombre', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('reservation_id', models.CharField(max_length=6)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotelBooking.room')),
            ],
        ),
    ]
