from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from travels.models import Trip, TripRequest, Location, Country, Commentary

User = get_user_model()


class TripModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="12345"
        )
        self.country = Country.objects.create(name="Germany", flag_name_img="de.png")
        self.location = Location.objects.create(
            name="Berlin", country=self.country, location_name_img="berlin.png"
        )

    def test_trip_str(self):
        trip = Trip.objects.create(
            owner=self.user,
            location=self.location,
            date=date.today() + timedelta(days=2),
            budget="$500-$1000",
            duration_trip="2-4 days",
            number_of_seats=5
        )
        self.assertEqual(str(trip), f"Trip to: {self.location}")

    def test_trip_clean_date_future(self):
        trip = Trip(
            owner=self.user,
            location=self.location,
            date=date.today() - timedelta(days=1),
            budget="$500-$1000",
            duration_trip="2-4 days",
            number_of_seats=5
        )
        with self.assertRaises(ValidationError):
            trip.clean()

    def test_is_finished(self):
        trip = Trip.objects.create(
            owner=self.user,
            location=self.location,
            date=date.today() - timedelta(days=1),
            budget="$500-$1000",
            duration_trip="2-4 days",
            number_of_seats=5
        )
        self.assertTrue(trip.is_finished())

    def test_can_comment(self):
        trip = Trip.objects.create(
            owner=self.user,
            location=self.location,
            date=date.today() - timedelta(days=2),
            budget="$500-$1000",
            duration_trip="2-4 days",
            number_of_seats=5
        )
        self.assertTrue(trip.can_comment(self.user))
        Commentary.objects.create(
            trip=trip, author_trip=self.user, recipient=self.user, text="Nice trip!"
        )
        self.assertFalse(trip.can_comment(self.user))


class TripRequestModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="12345"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="12345"
        )
        self.country = Country.objects.create(name="Germany", flag_name_img="de.png")
        self.location = Location.objects.create(
            name="Berlin", country=self.country, location_name_img="berlin.png"
        )
        self.trip = Trip.objects.create(
            owner=self.user,
            location=self.location,
            date=date.today() + timedelta(days=5),
            budget="$500-$1000",
            duration_trip="2-4 days",
            number_of_seats=1
        )

    def test_approve_request(self):
        request = TripRequest.objects.create(trip=self.trip, user=self.user2)
        request.approve()
        self.assertEqual(request.status, "approved")

    def test_reject_request(self):
        request = TripRequest.objects.create(trip=self.trip, user=self.user2)
        request.reject()
        self.assertEqual(request.status, "rejected")

    def test_approve_no_seats_available(self):
        request1 = TripRequest.objects.create(trip=self.trip, user=self.user2)
        request1.approve()
        request2 = TripRequest(trip=self.trip, user=self.user)
        with self.assertRaises(ValidationError):
            request2.approve()


class LocationCountryTests(TestCase):
    def test_location_str(self):
        country = Country.objects.create(name="Germany", flag_name_img="de.png")
        location = Location.objects.create(
            name="Berlin", country=country, location_name_img="berlin.png"
        )
        self.assertEqual(str(location), "Berlin (Germany)")

    def test_country_str(self):
        country = Country.objects.create(name="Germany", flag_name_img="de.png")
        self.assertEqual(str(country), "Germany")
