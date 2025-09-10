from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

from account.models import Profile

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match")
        return cd["password2"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class ProfileEditForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+380123456789"}
        )
    )
    date_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "telegram",
            "avatar",
            "gender",
            "date_birth",
            "about_me",
        ]
