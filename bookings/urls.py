
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_buses, name='search_buses'),

    # Seat selection
    path(
        'bus/<int:bus_id>/seats/',
        views.select_seats,
        name='select_seats'
    ),

    # Seat locking
    path(
        'seat/<int:seat_id>/lock/',
        views.lock_seat,
        name='lock_seat'
    ),

    # Passenger details
    path(
        'passenger/<int:bus_id>/',
        views.passenger_details,
        name='passenger_details'
    ),

    # Dummy payment
    path(
        'payment/',
        views.dummy_payment,
        name='dummy_payment'
    ),
    path(
    'verification/',
    views.booking_verification,
    name='booking_verification'
),
]
