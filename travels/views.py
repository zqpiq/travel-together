from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

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


class TripCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = FormTripCreateList
    success_url = reverse_lazy("travels:my-trips")
    template_name = "travels/trip_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyTripsListView(LoginRequiredMixin, generic.ListView):
    model = Trip

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)

class TripRequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = TripRequest
    fields = []
    template_name = "travels/join_trip_confirm.html"
    success_url = reverse_lazy("travels:home-page")

    def form_valid(self, form):
        trip = get_object_or_404(Trip, pk=self.kwargs["pk"])
        form.instance.trip = trip
        form.instance.user = self.request.user
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

class TripRequestApproveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        trip_request = TripRequest.objects.get(pk=pk)
        if trip_request != request.user:
            return JsonResponse({"error": "Not allowed"}, status=403)
        try:
            trip_request.approve()
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)
        return JsonResponse({"status": trip_request.status})

class TripRequestRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        trip_request = TripRequest.objects.get(pk=pk)
        if trip_request.trip.owner != request.user:
            return JsonResponse({"error": "Not allowed"}, status=403)
        trip_request.reject()
        return JsonResponse({"status": trip_request.status})
