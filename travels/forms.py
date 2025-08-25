from django import forms

from travels.models import Trip


class FormTripCreateList(forms.ModelForm):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )
    class Meta:
        model = Trip
        fields = ["location", "date", "budget", "description", "duration_trip", "number_of_seats"]
