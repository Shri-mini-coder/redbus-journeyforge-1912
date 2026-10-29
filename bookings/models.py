
from django.db import models


class Bus(models.Model):

    BUS_TYPE_CHOICES = [
        ("Seater", "Seater"),
        ("Sleeper", "Sleeper"),
        ("Semi-Sleeper", "Semi-Sleeper"),
    ]

    bus_name = models.CharField(max_length=100)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    journey_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField(default=40)

    # New field for bus type
    bus_type = models.CharField(
        max_length=20,
        choices=BUS_TYPE_CHOICES,
        default="Seater"
    )

    def __str__(self):
        return f"{self.bus_name}: {self.from_city} to {self.to_city}"



class Seat(models.Model):

    SEAT_TYPE_CHOICES = [
        ("Seater", "Seater"),
        ("Sleeper", "Sleeper"),
    ]

    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name="seats"
    )

    seat_number = models.CharField(max_length=5)

    # New field: regular seat or sleeper berth
    seat_type = models.CharField(
        max_length=20,
        choices=SEAT_TYPE_CHOICES,
        default="Seater"
    )

    is_booked = models.BooleanField(default=False)

    # Temporary seat-lock details
    locked_until = models.DateTimeField(null=True, blank=True)
    locked_by = models.CharField(max_length=40, blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bus", "seat_number"],
                name="unique_seat_per_bus"
            )
        ]

    def __str__(self):
        return f"{self.bus.bus_name} - {self.seat_number} ({self.seat_type})"


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bus", "seat_number"],
                name="unique_seat_per_bus"
            )
        ]

    def __str__(self):
        return f"{self.bus.bus_name} - Seat {self.seat_number}"
