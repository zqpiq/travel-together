from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from account.models import Profile

UserModel = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        user = UserModel.objects.create_user(
            username="testuser", email="testuser@example.com", password="12345"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("12345"))

    def test_unique_email(self):
        UserModel.objects.create_user(
            username="user1", email="unique@example.com", password="12345"
        )
        with self.assertRaises(Exception):
            UserModel.objects.create_user(
                username="user2", email="unique@example.com", password="12345"
            )


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="profileuser", email="profileuser@example.com", password="12345"
        )

    def test_create_profile(self):
        profile = Profile.objects.create(
            user=self.user,
            gender="Male",
            telegram="@profileuser",
            about_me="Hello world",
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.gender, "Male")
        self.assertEqual(profile.telegram, "@profileuser")
        self.assertEqual(profile.about_me, "Hello world")

    def test_profile_gender_default(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.gender, "N")

    def test_date_birth_validation_future(self):
        profile = Profile(
            user=self.user,
            date_birth=date.today() + timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            profile.clean()

    def test_date_birth_validation_past(self):
        past_date = date.today() - timedelta(days=365 * 20)
        profile = Profile(user=self.user, date_birth=past_date)
        try:
            profile.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for a past date_birth")
