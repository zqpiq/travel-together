from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "email", "date_joined"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "telegram", "gender", "about_me"]
