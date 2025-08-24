from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from account.forms import UserRegistrationForm, ProfileEditForm
from account.models import Profile


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            login(request, new_user)
            Profile.objects.create(user=new_user)
            return redirect("fill-profile")
    user_form = UserRegistrationForm()
    return render(
        request,
        "registration/register.html",
        {"user_form": user_form}
    )

def fill_profile(request: HttpRequest):
    if request.method == "POST":
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()
            return render(
                request,
                "registration/register_done.html",
                {"profile_form": profile_form}
            )
    profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "registration/profile_edit.html",
        {"profile_form": profile_form}
    )


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = "registration/profile_detail.html"

    def get_object(self):
        return self.request.user.profile


class PublicProfileDetailView(generic.DetailView):
    model = Profile
    template_name = "registration/public_profile_detail.html"
