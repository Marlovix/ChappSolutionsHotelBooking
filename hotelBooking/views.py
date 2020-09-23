import random
import string

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from datetime import date
from hotelBooking.models import Booking, Room, TypeRoom

# Create your views here.

global MIN_GUEST
global MAX_GUEST
global BOOKING_CODE_LENGHT

MIN_GUEST = 1
MAX_GUEST = 4
RESERVATION_CODE_LENGHT = 6

def bookings(request):
    bookings = []
    for booking in Booking.objects.all():
        bookings.append({
            'checkin':booking.checkin.strftime('%d/%m/%Y'),
            'checkout':booking.checkout.strftime('%d/%m/%Y'),
            'type_room':get_label_type_room(booking.room.type_room.id),
            'guests':booking.guests,
            'price':str(booking.price) + '€',
            'code':booking.code,
            'number':booking.room.number,
            'name':booking.name,
            'email':booking.email,
            'phone':booking.phone,
        })

    return render(request, 'bookings.html', {'bookings':bookings})

def searching_bookings(request):
    today = date.today().strftime('%Y-%m-%d')
    last = date(2020, 12, 31).strftime('%Y-%m-%d')
    return render(request, 'searching_bookings.html', {
        'min_date': today,
        'max_date': last,
        'options_guests': list(range(MIN_GUEST, MAX_GUEST+1))
        }
    )


def search(request):
    guests = int(request.POST.get('guests', 0))
    checkInStr = request.POST.get('checkin', None)
    checkOutStr = request.POST.get('checkout', None)

    # yyyy-mm-dd
    checkInDate = date(
        int(checkInStr[:-6]), int(checkInStr[5:-3]), int(checkInStr[8:]))
    checkOutDate = date(
        int(checkOutStr[:-6]), int(checkOutStr[5:-3]), int(checkOutStr[8:]))

    # days of booking
    daysBooking = abs(checkOutDate - checkInDate).days
    daysBookingStr = str(daysBooking) + ' día';
    if daysBooking != 1: daysBookingStr += 's'

    # Checkin the input data 
    if (checkInDate >= checkOutDate or
        guests < MIN_GUEST or
            guests > MAX_GUEST):
        return JsonResponse({'data': []})

    # Getting the rooms that are already in a booking
    takenRooms = Booking.objects.values(
        'room__id'
    ).filter(
        checkin__lt=checkOutDate,
        checkout__gt=checkInDate,
        room__type_room__max_guest__gte=guests
    )

    print(takenRooms)

    # Getting the rest of availble rooms
    rooms = Room.objects.values(
        'type_room_id',
        'type_room__price'
    ).filter(
        type_room__max_guest__gte=guests
    ).exclude(
        id__in=takenRooms
    ).annotate(
        available_rooms=Count('type_room_id')
    )

    # Formatting result data
    results = {
        'checkin':checkInDate.strftime('%Y-%m-%d'),
        'checkout':checkOutDate.strftime('%Y-%m-%d'),
        'checkin_view':checkInDate.strftime('%d/%m/%Y'),
        'checkout_view':checkOutDate.strftime('%d/%m/%Y'),
        'duration':daysBookingStr,
        'guests':guests,
        'rooms': []
    }

    # Formatting each room data
    for room in rooms:
        typeRoomStr = get_label_type_room(room['type_room_id'])
        availableRoomsStr = str(room['available_rooms']) + ' disponible'

        if room['available_rooms'] != 1:
            availableRoomsStr += 's'

        totalPrice = room['type_room__price'] * int(daysBooking)
        totalPriceStr = str(totalPrice) + '€'

        results['rooms'].append({
                'id_type_room': room['type_room_id'],
                'type_room': typeRoomStr,
                'available_rooms': availableRoomsStr,
                'total_price': totalPrice,
                'total_price_view': totalPriceStr
            }
        )

    return JsonResponse({'data': results})

def create_booking(request):
    checkIn = request.POST.get('checkin', None)
    checkOut = request.POST.get('checkout', None)
    guests = request.POST.get('guests', 0)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    price = request.POST.get('price', 0)
    typeRoom = request.POST.get('type_room', 0)

    # random code as resevation id
    code = get_random_string(RESERVATION_CODE_LENGHT)

    # Getting the rooms that are already in a booking
    takenRooms = Booking.objects.values(
        'room__id'
    ).filter(
        checkin__lt=checkOut,
        checkout__gt=checkIn,
        room__type_room__id=typeRoom
    )

    # Getting the rest of availble rooms
    room = Room.objects.filter(
        type_room__id=typeRoom
    ).exclude(
        id__in=takenRooms
    ).first()

    booking = Booking(
        checkin=checkIn, 
        checkout=checkOut, 
        guests=guests, 
        name=name, 
        email=email, 
        phone=phone, 
        price=price, 
        code=code,
        room=room)
    booking.save()

    return JsonResponse({'data': code})

def get_label_type_room(argument):
    labels = {
        1: "Habitación individual",
        2: "Habitación doble",
        3: "Habitación triple",
        4: "Habitación cuádruple"
    }
    return labels.get(argument, "Tipo de habitación desconocido")

# Random string (upper case)
def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length)).upper()