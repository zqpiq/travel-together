from django.contrib import admin

from travels.models import Trip, Location, Country, Commentary, TripRequest


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["owner", "location", "date", "budget"]

    def get_users(self, obj) -> str:
        return ", ".join([user.username for user in obj.user.all()])
    get_users.short_description = "Users"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "location_name_img"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "flag_name_img"]


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ["trip", "author_trip", "recipient", "created_at"]


@admin.register(TripRequest)
class TripRequestAdmin(admin.ModelAdmin):
    list_display = ["trip", "user", "status"]
