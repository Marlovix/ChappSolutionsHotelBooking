from django.db import models
from django.utils.timezone import now

# Create your models here.


class TypeRoom(models.Model):
    max_guest = models.IntegerField()
    price = models.IntegerField()


class Room(models.Model):
    number = models.CharField(max_length=2)
    type_room = models.ForeignKey(TypeRoom, on_delete=models.CASCADE)


class Booking(models.Model):
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.IntegerField()
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    price = models.IntegerField()
    code = models.CharField(max_length=6)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created = models.DateTimeField(default=now)
