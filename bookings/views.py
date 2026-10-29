
from datetime import datetime, timedelta

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Bus, Seat


def home(request):
    return render(request, 'bookings/home.html')


def search_buses(request):
    from_city = request.GET.get('from_city', '').strip()
    to_city = request.GET.get('to_city', '').strip()
    journey_date = request.GET.get('journey_date', '').strip()
    sort = request.GET.get('sort', 'departure_time')

    buses = Bus.objects.none()

    if from_city and to_city and journey_date:
        buses = Bus.objects.filter(
            from_city__iexact=from_city,
            to_city__iexact=to_city,
            journey_date=journey_date
        )

        if sort == 'price':
            buses = buses.order_by('price', 'departure_time')
        else:
            buses = buses.order_by('departure_time')

    for bus in buses:
        departure = datetime.combine(
            bus.journey_date, bus.departure_time
        )
        arrival = datetime.combine(
            bus.journey_date, bus.arrival_time
        )

        if arrival < departure:
            arrival += timedelta(days=1)

        duration = arrival - departure
        minutes = int(duration.total_seconds() // 60)
        bus.duration = f"{minutes // 60}h {minutes % 60}m"

    return render(request, 'bookings/search_results.html', {
        'buses': buses,
        'from_city': from_city,
        'to_city': to_city,
        'journey_date': journey_date,
        'sort': sort,
    })


def select_seats(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)

    if not bus.seats.exists():
        seat_numbers = [
            f"{row}{number}"
            for row in "ABCDEF"
            for number in range(1, 7)
        ]

        Seat.objects.bulk_create([
            Seat(bus=bus, seat_number=number)
            for number in seat_numbers
        ])

    seats = bus.seats.all().order_by('seat_number')

    return render(request, 'bookings/seat_selection.html', {
        'bus': bus,
        'seats': seats,
    })


@require_POST
def lock_seat(request, seat_id):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    now = timezone.now()

    with transaction.atomic():
        seat = Seat.objects.filter(id=seat_id).first()

        if seat is None:
            return JsonResponse({
                'success': False,
                'message': 'Seat not found.'
            }, status=404)

        if seat.is_booked:
            return JsonResponse({
                'success': False,
                'message': 'This seat is already booked.'
            }, status=409)

        if (
            seat.locked_until
            and seat.locked_until > now
            and seat.locked_by != session_key
        ):
            return JsonResponse({
                'success': False,
                'message': 'This seat is temporarily held by another user.'
            }, status=409)

        seat.locked_by = session_key
        seat.locked_until = now + timedelta(minutes=5)
        seat.save(update_fields=['locked_by', 'locked_until'])

    return JsonResponse({
        'success': True,
        'message': 'Seat held for five minutes.',
        'expires_at': seat.locked_until.isoformat(),
    })


def passenger_details(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'GET':
        seat_ids_text = request.GET.get('seat_ids', '')

        if seat_ids_text:
            try:
                seat_ids = [
                    int(value) for value in seat_ids_text.split(',')
                ]
            except ValueError:
                return redirect('select_seats', bus_id=bus.id)

            if not seat_ids or len(set(seat_ids)) != len(seat_ids):
                return redirect('select_seats', bus_id=bus.id)

            seats = Seat.objects.filter(
                bus=bus,
                id__in=seat_ids,
                is_booked=False,
                locked_by=request.session.session_key,
                locked_until__gt=timezone.now(),
            )

            if seats.count() != len(seat_ids):
                return redirect('select_seats', bus_id=bus.id)

            request.session['selected_seat_ids'] = list(
                seats.values_list('id', flat=True)
            )
            request.session['selected_bus_id'] = bus.id

        else:
            seat_ids = request.session.get('selected_seat_ids', [])

            if request.session.get('selected_bus_id') != bus.id or not seat_ids:
                return redirect('select_seats', bus_id=bus.id)

            seats = Seat.objects.filter(
                bus=bus,
                id__in=seat_ids,
                is_booked=False,
                locked_by=request.session.session_key,
                locked_until__gt=timezone.now(),
            )

            if seats.count() != len(seat_ids):
                return redirect('select_seats', bus_id=bus.id)

        return render(request, 'bookings/passenger_details.html', {
            'bus': bus,
            'seats': seats,
            'total': bus.price * seats.count(),
        })

    seat_ids = request.session.get('selected_seat_ids', [])

    if request.session.get('selected_bus_id') != bus.id or not seat_ids:
        return redirect('select_seats', bus_id=bus.id)

    seats = Seat.objects.filter(
        bus=bus,
        id__in=seat_ids,
        is_booked=False,
        locked_by=request.session.session_key,
        locked_until__gt=timezone.now(),
    )

    if seats.count() != len(seat_ids):
        return redirect('select_seats', bus_id=bus.id)

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()

    if not all([name, email, phone]):
        return render(request, 'bookings/passenger_details.html', {
            'bus': bus,
            'seats': seats,
            'total': bus.price * seats.count(),
            'error': 'Please fill in all passenger details.',
        })

    request.session['passenger_name'] = name
    request.session['passenger_email'] = email
    request.session['passenger_phone'] = phone

    return redirect('booking_verification')


def booking_verification(request):
    bus_id = request.session.get('selected_bus_id')
    seat_ids = request.session.get('selected_seat_ids', [])

    if not bus_id or not seat_ids:
        return redirect('home')

    if not all([
        request.session.get('passenger_name'),
        request.session.get('passenger_email'),
        request.session.get('passenger_phone'),
    ]):
        return redirect('passenger_details', bus_id=bus_id)

    bus = get_object_or_404(Bus, id=bus_id)

    seats = Seat.objects.filter(
        bus=bus,
        id__in=seat_ids,
        is_booked=False,
        locked_by=request.session.session_key,
        locked_until__gt=timezone.now(),
    )

    if seats.count() != len(seat_ids):
        return redirect('select_seats', bus_id=bus.id)

    return render(request, 'bookings/booking_verification.html', {
        'bus': bus,
        'seats': seats,
        'total': bus.price * seats.count(),
        'passenger_name': request.session['passenger_name'],
        'passenger_email': request.session['passenger_email'],
        'passenger_phone': request.session['passenger_phone'],
    })


def dummy_payment(request):
    if request.method != 'POST':
        return redirect('booking_verification')

    bus_id = request.session.get('selected_bus_id')
    seat_ids = request.session.get('selected_seat_ids', [])

    if not bus_id or not seat_ids:
        return redirect('home')

    bus = get_object_or_404(Bus, id=bus_id)

    with transaction.atomic():
        seats = Seat.objects.filter(
            bus=bus,
            id__in=seat_ids,
            is_booked=False,
            locked_by=request.session.session_key,
            locked_until__gt=timezone.now(),
        )

        if seats.count() != len(seat_ids):
            return redirect('select_seats', bus_id=bus.id)

        seats.update(
            is_booked=True,
            locked_by='',
            locked_until=None,
        )

        bus.available_seats = max(
            0, bus.available_seats - len(seat_ids)
        )
        bus.save(update_fields=['available_seats'])

    return render(request, 'bookings/booking_confirmation.html', {
        'bus': bus,
        'seats': list(Seat.objects.filter(
            bus=bus, id__in=seat_ids
        )),
        'total': bus.price * len(seat_ids),
        'passenger_name': request.session.get('passenger_name', ''),
    })