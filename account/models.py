from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    pass


class Profile(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("None", "Prefer not to say"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, null=True)
    telegram = models.CharField(max_length=35, blank=True, null=True)
    avatar = CloudinaryField("avatar", folder="profile_avatars", blank=True, null=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default="N")
    date_birth = models.DateField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
