from django.conf import settings
from django.db import models


class Trip(models.Model):
    BUDGET_CHOICES = (
        ("<#500", "<$500"),
        ("$500-$1000", "$500-$1000"),
        ("$1000-$3000", "$1000-$3000"),
        ("$3000-$5000", "$3000-$5000"),
        (">$5000", ">$5000"),
    )
    DURATION_CHOICES = (
        ("1 day", "1 day"),
        ("2-4 days", "2-4 days"),
        ("5-7 days", "5-7 days"),
        ("8-14 days", "8-15 days"),
        (">14 days", ">14 days"),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_trips")
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    date = models.DateField()
    budget = models.CharField(
        max_length=20,
        choices=BUDGET_CHOICES,
    )
    description = models.TextField(null=True, blank=True)
    duration_trip = models.CharField(max_length=9, choices=DURATION_CHOICES)
    number_of_seats = models.IntegerField()

    def __str__(self):
        return f"Trip to: {self.location}"


class TripRequest(models.Model):
    STATUS_CHOICES = (
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),

    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trip_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    contacts_visible = models.BooleanField(default=False)


    class Meta:
        unique_together = ("trip", "user")

    def approve(self):
        if self.trip.requests.filter(status="approved").count() < self.trip.number_of_seats:
            self.status = "approved"
            self.save()
        else:
            raise ValueError("No free seats available!")

    def reject(self):
        self.status = "rejected"
        self.save()

    def __str__(self):
        return f"Request by {self.user} for {self.trip}"


class Location(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="locations")
    location_name_img = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country.name})"


class Country(models.Model):
    name = models.CharField(max_length=50)
    flag_name_img = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Commentary(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_comments"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    RATING_CHOICE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICE
    )
