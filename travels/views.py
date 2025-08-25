from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib import messages

from account.models import Profile
from travels.forms import FormTripCreateList
from travels.models import Country, Location, Trip, TripRequest


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "travels/index.html")

class CountryListView(generic.ListView):
    model = Country


class LocationListView(generic.ListView):
    model = Location

    def get_queryset(self):
        try:
            country_id = self.kwargs["pk"]
            return Location.objects.filter(country_id=country_id)
        except KeyError:
            return Location.objects.all()


class TripListView(generic.ListView):
    model = Trip

    def get_queryset(self):
        try:
            location_id = self.kwargs["pk"]
            return Trip.objects.filter(location_id=location_id)
        except KeyError:
            return Trip.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_requests = TripRequest.objects.filter(user=self.request.user).values_list('trip_id', flat=True)
        context['user_trip_requests'] = user_requests
        return context


class TripCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = FormTripCreateList
    success_url = reverse_lazy("travels:my-trips")
    template_name = "travels/trip_form.html"

    def form_valid(self, form):
        user = self.request.user
        profile = getattr(user, "profile", None)

        if not user.email or not profile.phone_number:
            messages.error(
                self.request,
                "Please complete your profile (add email and phone number) before creating a trip."
            )
            return redirect("fill-profile")

        form.instance.owner = user
        return super().form_valid(form)


class MyTripsListView(LoginRequiredMixin, generic.ListView):
    model = Trip
    template_name = "travels/my_trips.html"

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)

class TripRequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = TripRequest
    fields = []
    template_name = "travels/join_trip_confirm.html"
    success_url = reverse_lazy("travels:home-page")


    def form_valid(self, form):
        user = self.request.user
        profile = getattr(user, "profile", None)

        if not user.email or not profile.phone_number:
            messages.error(
                self.request,
                "Please complete your profile (add email and phone number) before joining a trip."
            )
            return redirect("fill-profile")

        trip = get_object_or_404(Trip, pk=self.kwargs["pk"])
        form.instance.trip = trip
        form.instance.user = user
        return super().form_valid(form)

class TripRequestListView(LoginRequiredMixin, generic.ListView):
    model = TripRequest
    template_name = "travels/requests_list.html"
    context_object_name = "sent_requests"

    def get_queryset(self):
        return TripRequest.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["received_requests"] = TripRequest.objects.filter(trip__owner=self.request.user)
        return context


class TripRequestActionView(LoginRequiredMixin, View):
    def post(self, request, pk, action):
        trip_request = get_object_or_404(TripRequest, pk=pk)

        if trip_request.trip.owner != request.user:
            messages.error(request, "You cannot manage this request.")
            return redirect("travels:requests")

        if trip_request.status != "pending":
            messages.warning(request, "This request is already processed.")
            return redirect("travels:requests")

        try:
            if action == "approve":
                trip_request.approve()
                messages.success(request, f"Request approved ✅")
            elif action == "reject":
                trip_request.reject()
                messages.warning(request, f"Request rejected ❌")
            else:
                messages.error(request, "Unknown action.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect("travels:requests")
