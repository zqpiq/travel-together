from django.urls import path

from travels.views import (index,
                           CountryListView,
                           LocationListView,
                           TripListView, TripCreateView, MyTripsListView, TripRequestCreateView, TripRequestListView,
                           TripRequestActionView, CommentaryCreateView,
                           )

app_name ="travels"

urlpatterns = [
    path("", index, name="home-page"),
    path("countries/", CountryListView.as_view(), name="countries"),
    path("countries/locations/", LocationListView.as_view(), name="locations-all"),
    path("countries/<int:pk>/locations/", LocationListView.as_view(), name="locations"),
    path("trips/", TripListView.as_view(), name="trips-all"),
    path("locations/<int:pk>/trips", TripListView.as_view(), name="trips"),
    path("create-trip/", TripCreateView.as_view(), name="create-trip"),
    path("my-trips/", MyTripsListView.as_view(), name="my-trips"),
    path("trip/<int:pk>/join/", TripRequestCreateView.as_view(), name="join-trip"),
    path("requests/", TripRequestListView.as_view(), name="requests"),
    path(
        "request/<int:pk>/<str:action>/",
        TripRequestActionView.as_view(),
        name="request-action"
    ),
    path("trip/<int:pk>/add-comment/", CommentaryCreateView.as_view(), name="add-comment"),

]
