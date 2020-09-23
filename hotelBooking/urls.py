from django.urls import path
from hotelBooking import views

urlpatterns = [
    path('bookings/', views.bookings, name='Reservas'),
    path('searching_bookings/', views.searching_bookings, name='Reservar'),
    path('search/', views.search),
    path('create_booking/', views.create_booking),
]
